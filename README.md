# My FastAPI App

This project is a FastAPI application that provides an API for creating AWS S3 buckets. It is structured using a clean architecture approach, separating concerns into different layers: domain, use cases, infrastructure, and API.

## Project Structure

```
my-fastapi-app
├── src
│   ├── domain
│   │   ├── entities
│   │   │   └── bucket.py          # Defines the Bucket class
│   │   └── interfaces
│   │       └── storage_repository.py # Defines the StorageRepository interface
│   ├── use_cases
│   │   └── bucket_creation.py      # Contains the CreateBucketUseCase class
│   ├── infrastructure
│   │   ├── aws
│   │   │   └── s3_repository.py    # Implements the S3Repository class
│   │   └── config
│   │       └── aws_config.py       # Contains AWSSettings for configuration
│   └── api
│       ├── main.py                  # FastAPI application entry point
│       └── models
│           └── bucket_requests.py   # Defines request models for the API
└── README.md
```

## Installation

1. Clone the repository:
   ```
   git clone <repository-url>
   cd my-fastapi-app
   ```

2. Create a virtual environment and activate it:
   ```
   python -m venv venv
   source venv/bin/activate  # On Windows use `venv\Scripts\activate`
   ```

3. Install the required packages:
   ```
   pip install -r requirements.txt
   ```

## Configuration

Create a `.env` file in the root directory with the following content:

```
AWS_ACCESS_KEY=your_access_key
AWS_SECRET_KEY=your_secret_key
AWS_REGION=your_region
```

## Usage

To run the application, use the following command:

```
uvicorn src.api.main:app --reload
```

The API will be available at `http://127.0.0.1:8000`.

## API Endpoints

### Create Bucket

- **POST** `/bucket`
- **Request Body**:
  ```json
  {
    "bucket_name": "your_bucket_name"
  }
  ```
- **Response**:
  - Success: `{"message": "Bucket 'your_bucket_name' created successfully!"}`
  - Error: `{"detail": "Failed to create bucket"}`

## License

This project is licensed under the MIT License. See the LICENSE file for more details.