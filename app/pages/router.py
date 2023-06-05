from fastapi import APIRouter, Request
from fastapi.templating import Jinja2Templates


router = APIRouter(
    prefix="/pages",
    tags=["Frontend"],
)

templates = Jinja2Templates(directory="app/templates")

@router.get("/hotels")
async def get_hotels_page(
    request: Request
):
    return templates.TemplateResponse(name="hotels.html", context={"request": request})

