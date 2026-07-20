import logging
import os
from abc import ABC, abstractmethod
from typing import Dict, Any, List, Optional

logger = logging.getLogger(__name__)


class BaseModelInterface(ABC):
  @abstractmethod
  def load(self) -> bool:
      pass

  @abstractmethod
  def unload(self) -> bool:
      pass

  @abstractmethod
  def predict(self, payload: Dict[str, Any]) -> Dict[str, Any]:
      pass

  @abstractmethod
  def batch_predict(self, payloads: List[Dict[str, Any]]) -> List[Dict[str, Any]]:
      pass

  @abstractmethod
  def explain(self, payload: Dict[str, Any]) -> Dict[str, Any]:
      pass

  @abstractmethod
  def validate(self, payload: Dict[str, Any]) -> bool:
      pass

  @abstractmethod
  def version(self) -> str:
      pass

  @abstractmethod
  def metadata(self) -> Dict[str, Any]:
      pass

  @abstractmethod
  def health_check(self) -> bool:
      pass


class StandardizedModel(BaseModelInterface):
  """
  VIT standardized model wrapper.

  Load priority:
    1. Local .pkl file resolved from MODEL_DIR env var
    2. Reports is_loaded=False and raises on predict() if no artifact found
  """

  def __init__(self, model_id, model_version, storage_id=None, metadata_dict=None):
      self.model_id = model_id
      self.model_version = model_version
      self.storage_id = storage_id
      self._metadata = metadata_dict or {}
      self.is_loaded = False
      self._artifact = None

  def load(self) -> bool:
      model_dir = os.getenv("MODEL_DIR", "/app/models")
      candidates = [
          os.path.join(model_dir, f"{self.model_id}.pkl"),
          os.path.join(model_dir, f"{self.model_id}_v1.pkl"),
          os.path.join(model_dir, f"{self.model_id}_v2.pkl"),
      ]
      for path in candidates:
          if os.path.exists(path):
              try:
                  import joblib
                  self._artifact = joblib.load(path)
                  self.is_loaded = True
                  logger.info("Loaded artifact %s from %s", self.model_id, path)
                  return True
              except Exception as exc:
                  logger.warning("joblib load failed for %s: %s", self.model_id, exc)
                  break
      if not self.is_loaded:
          logger.warning(
              "No .pkl found for %s in %s — not loaded. "
              "Set MODEL_DIR and ensure .pkl files are in the Docker image.",
              self.model_id, model_dir,
          )
      return self.is_loaded

  def unload(self) -> bool:
      self._artifact = None
      self.is_loaded = False
      return True

  def predict(self, payload: Dict[str, Any]) -> Dict[str, Any]:
      if not self.is_loaded or self._artifact is None:
          raise RuntimeError(
              f"Model '{self.model_id}' not loaded. "
              "Check MODEL_DIR and ensure .pkl files are bundled in the Docker image."
          )
      try:
          import numpy as np
          features = payload.get("features", [])
          X = np.array(features).reshape(1, -1) if features else np.zeros((1, 1))
          if hasattr(self._artifact, "predict_proba"):
              proba = self._artifact.predict_proba(X)[0]
              return {"status": "success", "model_id": self.model_id,
                      "version": self.model_version, "prediction": float(proba.max()),
                      "probabilities": proba.tolist()}
          elif hasattr(self._artifact, "predict"):
              pred = self._artifact.predict(X)[0]
              return {"status": "success", "model_id": self.model_id,
                      "version": self.model_version, "prediction": float(pred)}
          raise RuntimeError(f"Artifact for '{self.model_id}' has no predict method")
      except Exception as exc:
          logger.error("Inference error for %s: %s", self.model_id, exc)
          raise

  def batch_predict(self, payloads):
      return [self.predict(p) for p in payloads]

  def explain(self, payload):
      return {"model_id": self.model_id, "explanation": "SHAP/LIME not yet wired"}

  def validate(self, payload):
      return "features" in payload

  def version(self):
      return self.model_version

  def metadata(self):
      return {"model_id": self.model_id, "version": self.model_version,
              "storage_id": self.storage_id, "is_loaded": self.is_loaded,
              "has_artifact": self._artifact is not None, **self._metadata}

  def health_check(self):
      return self.is_loaded and self._artifact is not None
