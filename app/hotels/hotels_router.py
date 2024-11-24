import asyncio
from datetime import date

from fastapi import APIRouter, Query, Request
from fastapi_cache.decorator import cache
from pydantic import TypeAdapter, parse_obj_as
from sqlalchemy.engine import Row

from app.hotels.hotels_dao import HotelsDAO, RoomsDAO
from app.hotels.hotels_shemas import SHotelsInfo, SRoomInfo

router = APIRouter(
    prefix='/hotels',
    tags=['Отели']
)


# @router.get('/{location}')
# @cache(expire=2000)
async def get_hotels_by_location_and_date(
        location: str,
        date_from: date,
        date_to: date
) -> list[SHotelsInfo]:
    # await asyncio.sleep(3)
    hotels = await HotelsDAO.search_for_hotels(location, date_from, date_to)

    # hotels_as_dicts = [dict(row._mapping) if isinstance(row, Row) else row for row in hotels]
    # hotels_json = parse_obj_as(list[SHotelsInfo], hotels_as_dicts)
    # return hotels_json
    return hotels


@router.get('/{hotel_id}/rooms')
async def get_rooms_by_date(
        hotel_id: int,
        date_from: date,
        date_to: date
) -> list[SRoomInfo]:

    rooms = await RoomsDAO.search_for_rooms(hotel_id, date_from, date_to)
    return rooms


async def get_all_rooms() -> list[SRoomInfo]:
    rooms = await RoomsDAO.find_all()
    return rooms