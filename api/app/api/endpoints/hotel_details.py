from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from app.db.session import get_db
from app.schemas.hotel import HotelDetail
from app.crud.hotel import fetch_hotel_detail
import logging

router = APIRouter()

@router.get("/hotel/{hotel_id}", response_model=HotelDetail)
async def get_hotel_details(
    hotel_id: int,
    search_id: int,
    db: Session = Depends(get_db)
):
    logging.info(f"Received request for hotel details. hotel_id: {hotel_id}, search_id: {search_id}")
    try:
        hotel_detail = fetch_hotel_detail(db, hotel_id)
        return hotel_detail
    except Exception as e:
        logging.error(f"Unexpected error occurred: {str(e)}")
        raise HTTPException(status_code=500, detail="Internal server error")