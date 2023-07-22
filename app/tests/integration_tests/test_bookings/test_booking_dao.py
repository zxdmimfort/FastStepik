from datetime import datetime

from app.bookings.dao import BookingDAO


async def test_add_and_get_booking():
    new_booking_id = await BookingDAO.add(
        user_id=2,
        room_id=2,
        date_from=datetime.strptime("2023-07-13", "%Y-%m-%d"),
        date_to=datetime.strptime("2023-07-25", "%Y-%m-%d"),
    )
    new_booking = await BookingDAO.find_by_id(new_booking_id)

    assert new_booking is not None
    assert new_booking.user_id == 2
    assert new_booking.room_id == 2


async def test_CRUD():
    new_booking_id = await BookingDAO.add(
        user_id=2,
        room_id=2,
        date_from=datetime.strptime("2023-01-01", "%Y-%m-%d"),
        date_to=datetime.strptime("2023-01-07", "%Y-%m-%d"),
    )

    new_booking = await BookingDAO.find_by_id(new_booking_id)
    assert new_booking

    await BookingDAO.delete_my_booking(new_booking_id, 2)

    new_booking = await BookingDAO.find_by_id(new_booking_id)
    assert not new_booking
