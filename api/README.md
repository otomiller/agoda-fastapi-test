# Hotel API

This project is a FastAPI-based API for managing hotel data and availability.

## Setup

1. Clone the repository:
   ```
   git clone https://github.com/your-username/hotel-api.git
   cd api
   ```

2. Create a virtual environment and activate it:
   ```
   python -m venv venv
   source venv/bin/activate  # On Windows, use `venv\Scripts\activate`
   ```

3. Install the required packages:
   ```
   pip install -r requirements.txt
   ```

4. Create a `.env` file in the project root and fill it with your configuration (use `.env.example` as a template).

<!-- 5. Initialize Alembic:
   ```
   alembic init alembic
   ``` -->

6. Generate an initial migration:
   ```
   alembic revision --autogenerate -m "Initial migration"
   ```

7. Apply the migration to set up the database:
   ```
   alembic upgrade head
   ```

## Running the Project

To run the project locally:

```
uvicorn app.main:app --reload
```

The API will be available at `http://localhost:8000`. You can access the API documentation at `http://localhost:8000/docs`.

## Testing

To run the tests:

```
pytest
```

## Project Structure

- `app/`: Main application package
  - `main.py`: FastAPI application instance and router inclusion
  - `api/`: API endpoints
  - `core/`: Core functionality (config, database)
  - `models/`: SQLAlchemy models
  - `schemas/`: Pydantic models for request/response
  - `services/`: Business logic
- `tests/`: Test files
- `alembic/`: Database migration files
- `alembic.ini`: Alembic configuration file

## Environment Variables

The following environment variables are required:

- `DB_NAME`: Database name
- `DB_USER`: Database user
- `DB_PASSWORD`: Database password
- `DB_HOST`: Database host
- `DB_PORT`: Database port
- `REDIS_URL`: Redis connection URL
- `AVAILABILITY_API_URL`: URL for the availability API
- `API_KEY`: API key for the availability API

These can be set in the `.env` file or in your environment.