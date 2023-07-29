from typing import Optional
from pydantic import BaseModel


class SHotels(BaseModel):
    id: Optional[int]
    name: str
    location: str
    services: list[str]
    rooms_quantity: int
    image_id: int


class SHotelsInfo(SHotels):
    rooms_left: int
