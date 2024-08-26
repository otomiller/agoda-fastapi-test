from fastapi import APIRouter, HTTPException, Depends
from sqlalchemy.ext.asyncio import AsyncSession
from app.core.database_config import get_db
from app.services import hotel_service
from app.schemas.hotel import HotelDetails

router = APIRouter()

@router.get("/hotel/{hotel_id}", response_model=HotelDetails)
async def get_hotel_details(hotel_id: int, search_id: str, db: AsyncSession = Depends(get_db)):
    try:
        hotel_details = await hotel_service.get_hotel_details(db, hotel_id, search_id)
        return hotel_details
    except Exception as e:
        raise HTTPException(status_code=404, detail=str(e))