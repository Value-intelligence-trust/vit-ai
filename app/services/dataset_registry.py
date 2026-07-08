from typing import List, Dict, Optional
from app.schemas.dataset import Dataset, DatasetCreate
from datetime import datetime, UTC

class DatasetRegistry:
    def __init__(self):
        self.datasets: Dict[str, Dataset] = {}

    def register(self, dataset_in: DatasetCreate) -> Dataset:
        dataset = Dataset(**dataset_in.model_dump())
        self.datasets[dataset.id] = dataset
        return dataset

    def get_all(self) -> List[Dataset]:
        return list(self.datasets.values())

    def get_by_id(self, dataset_id: str) -> Optional[Dataset]:
        return self.datasets.get(dataset_id)

    def delete(self, dataset_id: str) -> bool:
        if dataset_id in self.datasets:
            del self.datasets[dataset_id]
            return True
        return False

dataset_registry = DatasetRegistry()
