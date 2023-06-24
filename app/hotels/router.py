import asyncio
from datetime import date, datetime
from typing import Annotated
from fastapi import APIRouter, Query
from fastapi_cache.decorator import cache

from app.hotels.dao import HotelDAO
from app.hotels.schemas import SHotels, SHotelsInfo


router = APIRouter(
    prefix="/hotels",
    tags=["Отели & Комнаты"],
)


@router.get("", response_model=list[SHotelsInfo])
@cache(expire=30)
async def get_hotels_by_location_and_time(
    location: str,
    date_from: Annotated[date, Query(description=f"Например, {datetime.now().date()}")] = ...,
    date_to: Annotated[date, Query(description=f"Например, {datetime.now().date()}")] = ...,
):
    return await HotelDAO.find_all(location, date_from, date_to)


@router.get("/id/{hotel_id}", response_model=SHotels)
async def get_hotel_info(
    hotel_id: int
):
    return await HotelDAO.find_one_or_none(id=hotel_id)
