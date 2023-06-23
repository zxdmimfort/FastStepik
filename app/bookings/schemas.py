from datetime import date
from pydantic import BaseModel


class SBookings(BaseModel):
    id: int
    room_id: int
    user_id: int
    date_from: date
    date_to: date
    price: int
    total_cost: int
    total_days: int

class SBookingsInfo(SBookings):
    id_1: int
    hotel_id: int
    name: str
    description: str
    price_1: int
    services: list[str]
    quantity: int
    image_id: int
