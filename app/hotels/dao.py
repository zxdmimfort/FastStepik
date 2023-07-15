from datetime import date

from sqlalchemy import and_, func, or_, select
from app.bookings.models import Bookings
from app.dao.base import BaseDAO
from app.hotels.models import Hotels
from app.hotels.rooms.models import Rooms

from app.database import engine, async_session_maker


class HotelDAO(BaseDAO):
    model = Hotels

    @classmethod
    async def find_all(
        cls,
        location: str,
        date_from: date,
        date_to: date,
    ):
        """
        -- location = "Алтай"
        -- date_from = "2023-05-15"
        -- date_to = "2023-06-20"

        with booked_rooms as (
            select hotel_id, count(*) as already_booked
            from bookings
            join rooms on bookings.room_id = rooms.id
            join hotels on rooms.hotel_id = hotels.id
            where
            ((date_from >= '2023-05-15' and date_from <= '2023-06-20') or
            (date_from <= '2023-05-15' and date_to >= '2023-05-15'))
            group by hotel_id
        )
        select hotels.id, "name", "location", "services", rooms_quantity, image_id, rooms_quantity - coalesce(already_booked, 0) as rooms_left
        from hotels
        left join booked_rooms on hotels.id = booked_rooms.hotel_id
        where hotels.location like '%Алтай%'
        """
        booked_rooms = select(
            Rooms.hotel_id, func.count('*').label("already_booked")
        ).select_from(Bookings).join(
            Rooms, Rooms.id == Bookings.room_id).join(
            Hotels, Hotels.id == Rooms.hotel_id
        ).where(
            or_(
                and_(
                    Bookings.date_from >= date_from,
                    Bookings.date_from < date_to
                ),
                and_(
                    Bookings.date_from <= date_from,
                    Bookings.date_to > date_from
                )
            )
        ).group_by(Rooms.hotel_id).cte("booked_rooms")

        get_free_hotels = select(
            Hotels.id,
            Hotels.name,
            Hotels.location,
            Hotels.services,
            Hotels.rooms_quantity,
            Hotels.image_id,
            (Hotels.rooms_quantity - func.coalesce(booked_rooms.c.already_booked, 0)).label("rooms_left")
        ).select_from(Hotels).join(
            booked_rooms, booked_rooms.c.hotel_id == Hotels.id, isouter=True
        ).where(
            and_(
            Hotels.location.like(f"%{location}%"),
            (Hotels.rooms_quantity - func.coalesce(booked_rooms.c.already_booked, 0)) > 0
            )
        )

        # print(get_free_hotels.compile(engine, compile_kwargs={"literal_binds": True}))

        async with async_session_maker() as session:
            free_hotels = await session.execute(get_free_hotels)
            return free_hotels.mappings().all()

    @classmethod
    async def find_one(
        cls,
        hotel_id: int):

        get_selected_hotel = select(Hotels.__table__.columns).where(Hotels.id == hotel_id)

        async with async_session_maker() as session:
            selected_hotel = await session.execute(get_selected_hotel)
            return selected_hotel.mappings().one()
