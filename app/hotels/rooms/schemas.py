from pydantic import BaseModel, Json


class SRooms(BaseModel):
    id: int
    hotel_id: int
    name: str
    description: str
    price: int
    services: Json
    quantity: int
    image_id: int
