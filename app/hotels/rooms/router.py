from datetime import date
from app.hotels.rooms.dao import RoomDAO
from app.hotels.rooms.schemas import SRooms
from app.hotels.router import router


@router.get("/{hotel_id}/rooms", response_model=list[SRooms])
async def get_rooms(
    hotel_id: int,
    date_from: date,
    date_to: date,
):
    return await RoomDAO.find_all(hotel_id, date_from, date_to)
