from pydantic import BaseModel

class CreateBucketRequest(BaseModel):
    bucket_name: str

    # Only validate request format, not business rules
    class Config:
        min_length = 1  # Just ensure it's not empty