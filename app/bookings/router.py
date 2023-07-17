from datetime import date

from fastapi import APIRouter, BackgroundTasks, Depends
from pydantic import ValidationError, parse_obj_as

from app.bookings.dao import BookingDAO
from app.bookings.schemas import SBookings, SBookingsInfo
from app.tasks.tasks import send_booking_confirmation_email
from app.users.dependencies import get_current_user
from app.users.models import Users

router = APIRouter(
    prefix="/bookings",
    tags=["Бронирования"],
)


@router.get("", response_model=list[SBookingsInfo])
async def get_bookings(user: Users = Depends(get_current_user)):
    return await BookingDAO.find_all(user_id=user.id)


@router.post("", status_code=201, response_model=SBookings)
async def add_booking(
    background_tasks: BackgroundTasks,
    room_id: int,
    date_from: date,
    date_to: date,
    user: Users = Depends(get_current_user),
):
    booking = await BookingDAO.add(user.id, room_id, date_from, date_to)
    # try:
    # booking_dict = parse_obj_as(SBookings, booking).dict()
    # except ValidationError:
    #     pass
    # else:
    # вариант с celery
    # send_booking_confirmation_email.delay(booking_dict, user.email)
    # вариант с background tasks
    # background_tasks.add_task(send_booking_confirmation_email, booking_dict, user.email)
    return booking


@router.delete("/{booking_id}")
async def delete_booking(booking_id: int, user: Users = Depends(get_current_user)):
    await BookingDAO.delete_my_booking(booking_id=booking_id, user_id=user.id)
