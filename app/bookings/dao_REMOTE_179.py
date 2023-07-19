# DATA ACCESS OBJECT as dao.py or service.py or repo.py
# Обращаемся BookingDAO.find_all()

from datetime import date

from sqlalchemy import and_, delete, func, insert, or_, select

from app.bookings.models import Bookings
from app.dao.base import BaseDAO
from app.database import async_session_maker
from app.exceptions import BookingNotFound, RoomCannotBeBooked, UserNotEnoughPermissions
from app.hotels.rooms.models import Rooms


class BookingDAO(BaseDAO):
    model = Bookings

    @classmethod
    async def find_all(
        cls,
        user_id: int,
    ):
        get_bookings_with_info = (
            select(
                Bookings.__table__.columns,
                Rooms.hotel_id,
                Rooms.name,
                Rooms.description,
                Rooms.services,
                Rooms.quantity,
                Rooms.image_id,
            )
            .select_from(Bookings)
            .join(Rooms, Rooms.id == Bookings.room_id)
            .where(Bookings.user_id == user_id)
        )

        # print(get_bookings.compile(engine, compile_kwargs={"literal_binds": True}))
        async with async_session_maker() as session:
            bookings_with_info = await session.execute(get_bookings_with_info)
            return bookings_with_info.mappings().all()

    @classmethod
    async def add(
        cls,
        user_id: int,
        room_id: int,
        date_from: date,
        date_to: date,
    ):
        """
        with booked_rooms as (
                select * from bookings
                where room_id = 1 and (
                (date_from >= '2023-05-15' and date_from < '2023-06-20') or
            (date_from <= '2023-05-15' and date_to > '2023-05-15')
            )
        )
        select rooms.quantity - count(booked_rooms.room_id) from rooms
        left join booked_rooms on booked_rooms.room_id = rooms.id
        where rooms.id = 1
        group by rooms.quantity, booked_rooms.room_id
        """

        booked_rooms = (
            select(Bookings)
            .where(
                and_(
                    Bookings.room_id == room_id,
                    or_(
                        and_(
                            Bookings.date_from >= date_from,
                            Bookings.date_from < date_to,
                        ),
                        and_(
                            Bookings.date_from <= date_from,
                            Bookings.date_to > date_from,
                        ),
                    ),
                )
            )
            .cte("booked_rooms")
        )

        get_rooms_left = (
            select(
                (Rooms.quantity - func.count(booked_rooms.c.room_id)).label(
                    "rooms_left"
                )
            )
            .select_from(Rooms)
            .join(booked_rooms, booked_rooms.c.room_id == Rooms.id, isouter=True)
            .where(Rooms.id == room_id)
            .group_by(Rooms.quantity, booked_rooms.c.room_id)
        )

        # print(get_rooms_left.compile(engine, compile_kwargs={"literal_binds": True})) Компиляция в SQL

        async with async_session_maker() as session:
            rooms_left = await session.execute(get_rooms_left)
            rooms_left: int = rooms_left.scalar()

            if rooms_left <= 0:
                raise RoomCannotBeBooked
            get_price = select(Rooms.price).filter_by(id=room_id)
            price = await session.execute(get_price)
            price: int = price.scalar()
            add_booking = (
                insert(Bookings)
                .values(
                    room_id=room_id,
                    user_id=user_id,
                    date_from=date_from,
                    date_to=date_to,
                    price=price,
                )
                .returning(Bookings.id)
            )

            new_booking_id = await session.execute(add_booking)
            await session.commit()
            new_booking = await cls.find_one_or_none(id=new_booking_id.scalar())
            if not new_booking:
                raise BookingNotFound
            return new_booking

    @classmethod
    async def delete_my_booking(cls, booking_id: int, user_id: int):
        async with async_session_maker() as session:
            get_user_id_by_booking_id = (
                select(Bookings.user_id)
                .select_from(Bookings)
                .where(Bookings.id == booking_id)
            )

            user_id_by_booking_id = await session.execute(get_user_id_by_booking_id)
            user_id_by_booking_id: int = user_id_by_booking_id.scalar()

            if user_id_by_booking_id is None:
                raise BookingNotFound

            if user_id_by_booking_id != user_id:
                raise UserNotEnoughPermissions

            delete_booking_by_id = delete(Bookings).where(Bookings.id == booking_id)

            result = await session.execute(delete_booking_by_id)
            await session.commit()

            return result
