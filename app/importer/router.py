import codecs
import csv
import os
from tempfile import NamedTemporaryFile
import aiofiles
from fastapi import APIRouter, BackgroundTasks, Depends, File, UploadFile
from app.bookings.dao import BookingDAO
from app.bookings.schemas import SBookings
from app.exceptions import BookingNotFound, UserNotEnoughPermissions
from app.hotels.dao import HotelDAO
from app.hotels.rooms.dao import RoomDAO
from app.hotels.rooms.schemas import SRooms
from app.hotels.schemas import SHotels
from app.users.dao import UserDAO
from app.users.dependencies import get_current_user

from app.users.models import Users
from app.users.schemas import SUserAuth


router = APIRouter(
    prefix="/importer",
    tags=["Upload database"],
)


@router.post("/import/{database_name}", status_code=201)
async def import_data_to_database(database_name: str, file: UploadFile, user: Users = Depends(get_current_user)):
    if not user.admin:
        raise UserNotEnoughPermissions

    tables = {"bookings": (SBookings, BookingDAO, ('id', 'total_cost', 'total_days')), "hotels": (SHotels, HotelDAO, ('id',)), "rooms": (SRooms, RoomDAO, ('id',))}
    model, model_dao, pop_cols = tables.get(database_name, (None, None))
    if not model:
        raise BookingNotFound

    
    
    csvReader = csv.DictReader(codecs.iterdecode(file.file, 'utf-8'), delimiter=";")
    json_data = list(csvReader)
    file.file.close


    for row in json_data:
        print('||||importer.router.py|||||||||', type(row))
        if 'services' in row:
            row['services'] = []
        row = model(**row).dict()
        print(type(row))

        for pop_col in pop_cols:
            row.pop(pop_col, None)
        
        await model_dao.add(**row)
    
    return {"message": f"Successfuly upload {len(json_data)} data to {database_name}"}
