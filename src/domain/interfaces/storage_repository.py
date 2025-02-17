from abc import ABC, abstractmethod
from ..entities.bucket import Bucket

class StorageRepository(ABC):
    @abstractmethod
    async def create_bucket(self, bucket: Bucket) -> bool:
        pass