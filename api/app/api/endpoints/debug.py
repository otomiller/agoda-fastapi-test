from fastapi import APIRouter, Depends
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import text
from app.core.database import get_db

router = APIRouter()

@router.get("/debug/table_info")
async def get_table_info(db: AsyncSession = Depends(get_db)):
    query = text("SELECT column_name, data_type FROM information_schema.columns WHERE table_name = 'hotels';")
    result = await db.execute(query)
    columns = result.fetchall()
    return {"columns": [{"name": col[0], "type": col[1]} for col in columns]}

# Add this router to your main.py file