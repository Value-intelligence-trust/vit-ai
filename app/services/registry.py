from typing import List, Dict, Optional, Any
from app.schemas.model import Model, ModelCreate, ModelUpdate, ModelVersion, ModelVersionCreate
from app.services.base_model import StandardizedModel
from datetime import datetime, UTC
import logging

logger = logging.getLogger(__name__)

class ModelRegistry:
    def __init__(self):
        self.models: Dict[str, Model] = {}
        self.loaded_artifacts: Dict[str, StandardizedModel] = {} # In-memory model artifacts

    def register(self, model_in: ModelCreate) -> Model:
        version = ModelVersion(
            model_id=model_in.id,
            version=model_in.initial_version,
            storage_id=model_in.storage_id,
            status="active"
        )
        model = Model(
            **model_in.model_dump(exclude={"initial_version", "storage_id"}),
            versions=[version],
            active_version=model_in.initial_version
        )
        self.models[model.id] = model

        # Load standard model artifact
        storage_id = model_in.storage_id or f"local://models/{model.id}"
        self.load_model_artifact(model.id, version.version, storage_id)

        return model

    def load_model_artifact(self, model_id: str, version: str, storage_id: str):
        logger.info(f"Loading model artifact for {model_id} v{version} from {storage_id}")
        artifact = StandardizedModel(
            model_id=model_id,
            model_version=version,
            storage_id=storage_id
        )
        artifact.load()
        self.loaded_artifacts[f"{model_id}:{version}"] = artifact

    def get_artifact(self, model_id: str, version: str) -> Optional[StandardizedModel]:
        return self.loaded_artifacts.get(f"{model_id}:{version}")

    def get_all(self) -> List[Model]:
        return list(self.models.values())

    def get_by_id(self, model_id: str) -> Optional[Model]:
        return self.models.get(model_id)

    def add_version(self, model_id: str, version_in: ModelVersionCreate) -> Optional[ModelVersion]:
        model = self.get_by_id(model_id)
        if not model:
            return None
        version = ModelVersion(model_id=model_id, **version_in.model_dump())
        model.versions.append(version)
        model.updated_at = datetime.now(datetime.UTC)

        storage_id = version.storage_id or f"local://models/{model_id}-{version.version}"
        self.load_model_artifact(model_id, version.version, storage_id)

        return version

    def update(self, model_id: str, model_in: ModelUpdate) -> Optional[Model]:
        if model_id not in self.models:
            return None
        model = self.models[model_id]
        update_data = model_in.model_dump(exclude_unset=True)
        for field, value in update_data.items():
            setattr(model, field, value)
        model.updated_at = datetime.now(datetime.UTC)
        return model

    def delete(self, model_id: str) -> bool:
        if model_id in self.models:
            del self.models[model_id]
            if f"{model_id}:" in "".join(self.loaded_artifacts.keys()):
                keys_to_del = [k for k in self.loaded_artifacts.keys() if k.startswith(f"{model_id}:")]
                for k in keys_to_del:
                    self.loaded_artifacts[k].unload()
                    del self.loaded_artifacts[k]
            return True
        return False

registry = ModelRegistry()
