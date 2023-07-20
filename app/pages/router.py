from fastapi import APIRouter, Depends, Request
from fastapi.templating import Jinja2Templates

from app.hotels.router import get_hotels_by_location_and_time
from app.users.router import get_my_info

router = APIRouter(
    prefix="/pages",
    tags=["Frontend"],
)

templates = Jinja2Templates(directory="app/templates")


@router.get("/hotels")
async def get_hotels_page(
    request: Request, hotels=Depends(get_hotels_by_location_and_time)
):
    return templates.TemplateResponse(
        name="hotels.html", context={"request": request, "hotels": hotels}
    )


@router.get("/auth_me")
async def get_my_page(request: Request, user_info=Depends(get_my_info)):
    return templates.TemplateResponse(
        name="person_account.html", context={"request": request, "user_info": user_info}
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
