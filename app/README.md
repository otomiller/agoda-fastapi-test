# Agoda API

This FastAPI application retrieves hotel data from a PostgreSQL database and serves it through API endpoints.

## Installation and Setup

### 1. Clone the Repository

```bash
git clone https://github.com/your-username/agoda-api.git
cd agoda-api
```

### 2. Create and Activate a Virtual Environment
```
python3 -m venv venv
source venv/bin/activate
```

### To start the FastAPI server:

```
uvicorn app.main:app --reload
```


## API Endpoints

### 1. Get List of Hotels

- **Endpoint**: `/hotels`
- **Method**: GET
- **Description**: Returns a list of hotels with pagination.

### 2. Get Hotel Details by ID

- **Endpoint**: `/hotels/{hotel_id}`
- **Method**: GET
- **Description**: Retrieves detailed information about a hotel by its ID.


### Usage Example

To fetch hotel data, make a GET request to the following endpoint:

```
curl http://127.0.0.1:8000/hotels/1
```

