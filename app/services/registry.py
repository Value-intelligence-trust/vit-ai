from typing import List, Dict, Optional, Any
from app.schemas.model import Model, ModelCreate, ModelUpdate, ModelVersion, ModelVersionCreate
from app.services.base_model import StandardizedModel
from datetime import datetime, UTC
import logging

logger = logging.getLogger(__name__)

VIT_CORE_MODELS = [
  {"id": "xgb_v1",          "name": "XGBoost Ensemble",      "version": "1.0", "type": "classification"},
  {"id": "lstm_v1",          "name": "LSTM Sequential",        "version": "1.0", "type": "sequential"},
  {"id": "transformer_v1",   "name": "Transformer Attention",  "version": "1.0", "type": "transformer"},
  {"id": "rf_v1",            "name": "Random Forest",          "version": "1.0", "type": "classification"},
  {"id": "gbm_v1",           "name": "Gradient Boosting",      "version": "1.0", "type": "classification"},
  {"id": "bayes_v1",         "name": "Bayesian Network",       "version": "1.0", "type": "probabilistic"},
  {"id": "logistic_v1",      "name": "Logistic Regression",    "version": "1.0", "type": "classification"},
  {"id": "elo_v1",           "name": "ELO Rating System",      "version": "1.0", "type": "rating"},
  {"id": "poisson_v1",       "name": "Poisson Regressor",      "version": "1.0", "type": "regression"},
  {"id": "dixon_coles_v1",   "name": "Dixon-Coles",            "version": "1.0", "type": "probabilistic"},
  {"id": "hybrid_v1",        "name": "Hybrid Ensemble",        "version": "1.0", "type": "ensemble"},
  {"id": "market_v1",        "name": "Market Odds Model",      "version": "1.0", "type": "market"},
  {"id": "ensemble_v1",      "name": "Master Ensemble",        "version": "1.0", "type": "ensemble"},
  {"id": "btts_v2",          "name": "BTTS Model v2",          "version": "2.0", "type": "classification"},
  {"id": "over_under_v2",    "name": "Over/Under v2",          "version": "2.0", "type": "classification"},
  {"id": "correct_score_v2", "name": "Correct Score v2",       "version": "2.0", "type": "classification"},
]


class ModelRegistry:
  def __init__(self):
      self.models: Dict[str, Model] = {}
      self.loaded_artifacts: Dict[str, StandardizedModel] = {}

  def bootstrap_vit_models(self) -> int:
      loaded = 0
      for spec in VIT_CORE_MODELS:
          try:
              model_in = ModelCreate(
                  id=spec["id"], name=spec["name"],
                  description=f"VIT core model — {spec['type']}",
                  model_type=spec["type"], initial_version=spec["version"], storage_id=None,
              )
              self.register(model_in)
              artifact = self.get_artifact(spec["id"], spec["version"])
              if artifact and artifact.is_loaded:
                  loaded += 1
          except Exception as exc:
              logger.warning("Bootstrap failed for %s: %s", spec["id"], exc)
      if loaded == 0:
          logger.error(
              "STARTUP ASSERTION FAILED: 0/%d models loaded. "
              "Verify MODEL_DIR and that .pkl files are bundled in the Docker image.",
              len(VIT_CORE_MODELS),
          )
      else:
          logger.info("STARTUP: %d/%d VIT models loaded.", loaded, len(VIT_CORE_MODELS))
      return loaded

  def register(self, model_in: ModelCreate) -> Model:
      version = ModelVersion(model_id=model_in.id, version=model_in.initial_version,
                             storage_id=model_in.storage_id, status="active")
      model = Model(**model_in.model_dump(exclude={"initial_version", "storage_id"}),
                    versions=[version], active_version=model_in.initial_version)
      self.models[model.id] = model
      storage_id = model_in.storage_id or f"local://models/{model.id}"
      self.load_model_artifact(model.id, version.version, storage_id)
      return model

  def load_model_artifact(self, model_id: str, version: str, storage_id: str):
      artifact = StandardizedModel(model_id=model_id, model_version=version, storage_id=storage_id)
      artifact.load()
      self.loaded_artifacts[f"{model_id}:{version}"] = artifact

  def get_artifact(self, model_id: str, version: str) -> Optional[StandardizedModel]:
      return self.loaded_artifacts.get(f"{model_id}:{version}")

  def get_all(self) -> List[Model]:
      return list(self.models.values())

  def get_by_id(self, model_id: str) -> Optional[Model]:
      return self.models.get(model_id)

  def loaded_model_count(self) -> int:
      return sum(1 for a in self.loaded_artifacts.values() if a.is_loaded)

  def add_version(self, model_id: str, version_in: ModelVersionCreate) -> Optional[ModelVersion]:
      model = self.get_by_id(model_id)
      if not model:
          return None
      version = ModelVersion(model_id=model_id, **version_in.model_dump())
      model.versions.append(version)
      model.updated_at = datetime.now(UTC)
      self.load_model_artifact(model_id, version.version,
                               version.storage_id or f"local://models/{model_id}-{version.version}")
      return version

  def update(self, model_id: str, model_in: ModelUpdate) -> Optional[Model]:
      if model_id not in self.models:
          return None
      model = self.models[model_id]
      for field, value in model_in.model_dump(exclude_unset=True).items():
          setattr(model, field, value)
      model.updated_at = datetime.now(UTC)
      return model

  def delete(self, model_id: str) -> bool:
      if model_id in self.models:
          del self.models[model_id]
          for k in [k for k in self.loaded_artifacts if k.startswith(f"{model_id}:")]:
              del self.loaded_artifacts[k]
          return True
      return False
