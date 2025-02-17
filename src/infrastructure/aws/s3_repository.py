import boto3
from botocore.exceptions import ClientError
from ...domain.interfaces.storage_repository import StorageRepository
from ...domain.entities.bucket import Bucket
from ..config.aws_config import AWSSettings

class S3Repository(StorageRepository):
    def __init__(self, settings: AWSSettings):
        self.settings = settings
        
    async def create_bucket(self, bucket: Bucket) -> bool:
        try:
            if self.settings.AWS_REGION == "us-east-1":
                s3_client = boto3.client(
                    "s3",
                    aws_access_key_id=self.settings.AWS_ACCESS_KEY,
                    aws_secret_access_key=self.settings.AWS_SECRET_KEY
                )
                s3_client.create_bucket(Bucket=bucket.name)
            else:
                s3_client = boto3.client(
                    "s3",
                    aws_access_key_id=self.settings.AWS_ACCESS_KEY,
                    aws_secret_access_key=self.settings.AWS_SECRET_KEY,
                    region_name=self.settings.AWS_REGION
                )
                s3_client.create_bucket(
                    Bucket=bucket.name,
                    CreateBucketConfiguration={
                        "LocationConstraint": self.settings.AWS_REGION
                    }
                )
            return True
        except ClientError as e:
            print(f"ClientError creating bucket: {e}")
            return False