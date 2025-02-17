from pydantic import BaseModel

class CreateBucketRequest(BaseModel):
    bucket_name: str