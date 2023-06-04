from datetime import date

from sqlalchemy import and_, func, or_, select
from app.bookings.models import Bookings
from app.dao.base import BaseDAO
from app.hotels.rooms.models import Rooms

from app.database import engine, async_session_maker


class RoomDAO(BaseDAO):
    model = Rooms

    @classmethod
    async def find_all(
        cls,
        hotel_id: int,
        date_from: date,
        date_to: date,
    ):
        """
        -- hotel_id = 4
        -- date_from = "2023-05-10"
        -- date_to = "2023-06-20"

        with booked_rooms as (
            select room_id, count(*) as already_booked from bookings
            where (date_from >= '2023-05-10' and date_from <= '2023-06-20') or
            (date_from <= '2023-05-10' and date_to >= '2023-05-10')
            group by room_id
        )


        select
            rooms.id,
            hotel_id,
            rooms.name,
            description,
            services,
            price,
            quantity,
            image_id,
            (date('2023-06-20') - date('2023-05-10')) * price as total_cost,
            greatest(quantity - coalesce(already_booked, 0), 0) as rooms_left
        from rooms left join
        booked_rooms on rooms.id = booked_rooms.room_id
        where greatest(quantity - coalesce(already_booked, 0), 0) > 0 and hotel_id = 1
        order by id;
        """
        booked_rooms = select(
            Bookings.room_id,
            func.count('*').label("already_booked")
            ).select_from(Bookings).where(
                or_(
                    and_(
                        date_from >= Bookings.date_from,
                        date_from <= Bookings.date_to
                    ),
                    and_(
                        date_from <= Bookings.date_from,
                        date_to >= Bookings.date_from
                    )
                )
            ).group_by(Bookings.room_id).cte("booked_rooms")

        get_free_rooms = select(
            Rooms.id, Rooms.hotel_id, Rooms.description,
            Rooms.services, Rooms.price, Rooms.quantity,
            Rooms.image_id,
            ((func.date(date_to) - func.date(date_from)) * Rooms.price).label("total_cost"),
            func.greatest((Rooms.quantity - func.coalesce(booked_rooms.c.already_booked, 0)), 0).label("rooms_left")
        ).select_from(Rooms).join(
            booked_rooms, booked_rooms.c.room_id == Rooms.id, isouter=True
        ).where(
            and_(
                Rooms.hotel_id == hotel_id,
                func.greatest((Rooms.quantity - func.coalesce(booked_rooms.c.already_booked, 0)), 0) > 0
            )
        )
        
        # print(get_free_rooms.compile(engine, compile_kwargs={"literal_binds": True}))

        async with async_session_maker() as session:
            free_rooms = await session.execute(get_free_rooms)
            return free_rooms.mappings().all()