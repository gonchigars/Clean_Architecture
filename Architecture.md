### Clean Architecture Layers

The project follows Clean Architecture's concentric circles, from innermost to outermost:

1. **Domain Layer** (`domain/`)

```python
# domain/entities/bucket.py
@dataclass
class Bucket:
    name: str
    region: str
    created_at: datetime = datetime.now()

    def validate(self) -> bool:
        return bool(self.name and self.region)
```

This represents the core business rules. The `Bucket` entity knows nothing about AWS or S3 - it's a pure domain concept. The validation rules are business rules that exist regardless of how we store the bucket.

2. **Use Cases** (`use_cases/`)

```python
class CreateBucketUseCase:
    def __init__(self, storage_repository: StorageRepository):
        self.storage_repository = storage_repository

    async def execute(self, bucket_name: str, region: str) -> bool:
        bucket = Bucket(name=bucket_name, region=region)
        if not bucket.validate():
            raise ValueError("Invalid bucket configuration")
        return await self.storage_repository.create_bucket(bucket)
```

This layer contains application-specific business rules. Notice how it depends on the `StorageRepository` interface, not the concrete AWS implementation. This follows the Dependency Inversion Principle.

3. **Interface Adapters** (`infrastructure/` and `api/`)

```python
class S3Repository(StorageRepository):
    def __init__(self, settings: AWSSettings):
        self.settings = settings

    async def create_bucket(self, bucket: Bucket) -> bool:
        # AWS-specific implementation
```

This layer converts data between the use cases and external agencies (AWS S3 in this case).

### SOLID Principles Application

1. **Single Responsibility Principle (SRP)**
   Each class has one reason to change:

- `Bucket` handles bucket validation
- `S3Repository` handles AWS interactions
- `CreateBucketUseCase` orchestrates the creation flow
- `AWSSettings` manages configuration

2. **Open/Closed Principle (OCP)**

```python
# domain/interfaces/storage_repository.py
class StorageRepository(ABC):
    @abstractmethod
    async def create_bucket(self, bucket: Bucket) -> bool:
        pass
```

We can add new storage implementations (like Azure or GCP) without modifying existing code.

3. **Liskov Substitution Principle (LSP)**
   Any storage repository implementation can be used interchangeably:

```python
# Could use any of these:
repository = S3Repository(settings)
repository = MockRepository()
repository = InMemoryRepository()
```

4. **Interface Segregation Principle (ISP)**
   The repository interface is focused and minimal. If we needed other operations, we'd create separate interfaces:

```python
class BucketReader(ABC):
    @abstractmethod
    async def get_bucket(self, name: str) -> Bucket:
        pass

class BucketWriter(ABC):
    @abstractmethod
    async def create_bucket(self, bucket: Bucket) -> bool:
        pass
```

5. **Dependency Inversion Principle (DIP)**
   High-level modules (use cases) depend on abstractions (repository interface), not concrete implementations (S3).

### Design Patterns Used

1. **Repository Pattern**

```python
class S3Repository(StorageRepository):
    # Abstracts data storage details
```

2. **Dependency Injection**

```python
def get_bucket_use_case(
    repository: S3Repository = Depends(get_storage_repository)
) -> CreateBucketUseCase:
    return CreateBucketUseCase(repository)
```

3. **Factory Method** (in dependencies)

```python
def get_storage_repository(settings: AWSSettings = Depends(get_settings)) -> S3Repository:
    return S3Repository(settings)
```

### Error Handling Strategy

The application uses a layered error handling approach:

1. **Domain Layer**: Business rule violations

```python
def validate(self) -> bool:
    return bool(self.name and self.region)
```

2. **Use Case Layer**: Application errors

```python
if not bucket.validate():
    raise ValueError("Invalid bucket configuration")
```

3. **Infrastructure Layer**: Technical errors

```python
try:
    s3_client.create_bucket(...)
except ClientError as e:
    print(f"ClientError creating bucket: {e}")
    return False
```

4. **API Layer**: HTTP-specific errors

```python
if not success:
    raise HTTPException(status_code=500, detail="Failed to create bucket")
```

### Configuration Management

The application uses Pydantic for type-safe configuration:

```python
class AWSSettings(BaseSettings):
    AWS_ACCESS_KEY: str
    AWS_SECRET_KEY: str
    AWS_REGION: str

    class Config:
        env_file = ".env"
```

This structure provides several benefits:

- Testability: Easy to mock dependencies
- Maintainability: Clear separation of concerns
- Flexibility: Easy to change implementations
- Security: Configuration isolated from business logic
- Scalability: Easy to add new features or storage providers

The code follows both strategic patterns (Clean Architecture) and tactical patterns (SOLID, design patterns) to create a maintainable and extensible system.
