from datetime import date
from fastapi import APIRouter

from app.hotels.dao import HotelDAO
from app.hotels.schemas import SHotels


router = APIRouter(
    prefix="/hotels",
    tags=["Отели & Комнаты"],
)


@router.get("")
async def get_hotels_by_location_and_time(
    location: str,
    date_from: date,
    date_to: date,
):
    return await HotelDAO.find_all(location, date_from, date_to)


@router.get("/id/{hotel_id}", response_model=SHotels)
async def get_hotel_info(
    hotel_id: int
):
    return await HotelDAO.find_one(hotel_id)
