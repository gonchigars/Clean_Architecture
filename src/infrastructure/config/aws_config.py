from pydantic_settings import BaseSettings

class AWSSettings(BaseSettings):
    AWS_ACCESS_KEY: str
    AWS_SECRET_KEY: str
    AWS_REGION: str

    class Config:
        env_file = ".env"