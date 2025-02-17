from ..domain.entities.bucket import Bucket
from ..domain.interfaces.storage_repository import StorageRepository

class CreateBucketUseCase:
    def __init__(self, storage_repository: StorageRepository):
        self.storage_repository = storage_repository

    async def execute(self, bucket_name: str, region: str) -> bool:
        bucket = Bucket(name=bucket_name, region=region)
        
        if not bucket.validate():
            raise ValueError("Invalid bucket configuration")
            
        return await self.storage_repository.create_bucket(bucket)