from fastapi import APIRouter
from app.api.endpoints import hotel_search, hotel_details

api_router = APIRouter()
api_router.include_router(hotel_search.router, prefix="/hotels", tags=["hotels"])
api_router.include_router(hotel_details.router, prefix="/hotels", tags=["hotels"])