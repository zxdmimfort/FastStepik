from fastapi import APIRouter, Depends, Request
from fastapi.templating import Jinja2Templates
from app.hotels.rooms.router import get_rooms

from app.hotels.router import get_hotels_by_location_and_time


router = APIRouter(
    prefix="/pages",
    tags=["Frontend"],
)

templates = Jinja2Templates(directory="app/templates")

@router.get("/hotels")
async def get_hotels_page(
    request: Request,
    hotels=Depends(get_hotels_by_location_and_time)
):
    return templates.TemplateResponse(
        name="hotels.html",
        context={"request": request, "hotels": hotels}
    )

# @router.get("/{hotel_id}/rooms")
# async def get_hotel_rooms_page(
#     request: Request,
#     rooms=Depends()
# ):
#     return templates.TemplateResponse(
#         name="rooms.html",
#         context={"request": request, "rooms": rooms}
#     )

