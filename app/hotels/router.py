from datetime import date, datetime, timedelta
from typing import Annotated

from fastapi import APIRouter, Query
from fastapi_cache.decorator import cache

from app.exceptions import BackToTheFuture, BookingNotFound, TooLongBooking
from app.hotels.dao import HotelDAO
from app.hotels.schemas import SHotels, SHotelsInfo

router = APIRouter(
    prefix="/hotels",
    tags=["Отели & Комнаты"],
)


@router.get("", response_model=list[SHotelsInfo])
@cache(expire=30)
async def get_hotels_by_location_and_time(
    location: Annotated[
        str,
        Query(
            description="Например, Алтай",
        ),
    ],
    date_from: Annotated[
        date, Query(description=f"Например, {datetime.now().date()}")
    ] = ...,
    date_to: Annotated[
        date, Query(description=f"Например, {datetime.now().date()}")
    ] = ...,
):
    if date_from > date_to:
        raise BackToTheFuture
    if date_to - date_from > timedelta(days=30):
        raise TooLongBooking

    return await HotelDAO.find_all(location, date_from, date_to)


@router.get("/id/{hotel_id}", response_model=SHotels)
async def get_hotel_info(hotel_id: int):
    result = await HotelDAO.find_one_or_none(id=hotel_id)
    if result:
        return result
    raise BookingNotFound
