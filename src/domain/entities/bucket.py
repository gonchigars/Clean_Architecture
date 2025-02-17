from dataclasses import dataclass
from datetime import datetime

class DomainValidationError(Exception):
    pass

@dataclass
class Bucket:
    name: str
    region: str
    created_at: datetime = datetime.now()

    def validate(self) -> bool:
        # Business rule validations
        if not self._is_valid_bucket_name(self.name):
            raise DomainValidationError("Bucket name must be between 3 and 63 characters")
        
        if not self._is_valid_region(self.region):
            raise DomainValidationError("Invalid AWS region")
        
        return True

    @staticmethod
    def _is_valid_bucket_name(name: str) -> bool:
        # AWS S3 bucket naming rules
        return (len(name) >= 3 and len(name) <= 63 and 
                name.islower() and name.isalnum())

    @staticmethod
    def _is_valid_region(region: str) -> bool:
        valid_regions = ['us-east-1', 'eu-west-1']  # etc
        return region in valid_regions

