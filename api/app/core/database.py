from app.core.database_config import AsyncSessionLocal
from sqlalchemy.exc import SQLAlchemyError

async def get_db():
    try:
        async with AsyncSessionLocal() as session:
            yield session
    except SQLAlchemyError as e:
        print(f"Database error: {e}")
        raise
    finally:
        await session.close()