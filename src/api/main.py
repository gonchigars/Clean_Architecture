from fastapi import FastAPI, HTTPException, Depends
from .models.bucket_requests import CreateBucketRequest
from ..infrastructure.config.aws_config import AWSSettings
from ..infrastructure.aws.s3_repository import S3Repository
from ..use_cases.bucket_creation import CreateBucketUseCase

app = FastAPI()

def get_settings() -> AWSSettings:
    return AWSSettings()

def get_storage_repository(settings: AWSSettings = Depends(get_settings)) -> S3Repository:
    return S3Repository(settings)

def get_bucket_use_case(
    repository: S3Repository = Depends(get_storage_repository)
) -> CreateBucketUseCase:
    return CreateBucketUseCase(repository)

@app.post("/bucket")
async def create_bucket_endpoint(
    request: CreateBucketRequest,
    use_case: CreateBucketUseCase = Depends(get_bucket_use_case),
    settings: AWSSettings = Depends(get_settings)
):
    if not request.bucket_name:
        raise HTTPException(status_code=400, detail="Bucket name cannot be empty")

    success = await use_case.execute(request.bucket_name, settings.AWS_REGION)
    
    if not success:
        raise HTTPException(status_code=500, detail="Failed to create bucket")
        
    return {"message": f"Bucket '{request.bucket_name}' created successfully!"}