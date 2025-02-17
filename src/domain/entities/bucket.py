from dataclasses import dataclass
from datetime import datetime

@dataclass
class Bucket:
    name: str
    region: str
    created_at: datetime = datetime.now()

    def validate(self) -> bool:
        return bool(self.name and self.region)