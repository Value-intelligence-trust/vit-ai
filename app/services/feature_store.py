from typing import List, Dict, Optional
from app.schemas.feature import Feature, FeatureCreate
from datetime import datetime, UTC

class FeatureStore:
    def __init__(self):
        self.features: Dict[str, Feature] = {}

    def register(self, feature_in: FeatureCreate) -> Feature:
        feature = Feature(**feature_in.model_dump())
        self.features[feature.id] = feature
        return feature

    def get_all(self) -> List[Feature]:
        return list(self.features.values())

    def get_by_id(self, feature_id: str) -> Optional[Feature]:
        return self.features.get(feature_id)

feature_store = FeatureStore()
