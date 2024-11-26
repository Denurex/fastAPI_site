
from datetime import datetime
from encodings import utf_8

import pytest
from hotels.hotels_dao import HotelsDAO, RoomsDAO
from PIL.PdfParser import encode_text


@pytest.mark.parametrize('location,date_from,date_to',[
    ('Алтай', '2023-06-10', '2023-06-20'),
    ('Атай', '2023-06-10', '2023-06-20')
])
async def test_search_for_hotels(location, date_from, date_to):
    hotels = await HotelsDAO.search_for_hotels(
        location,
        date_from=datetime.strptime(date_from, '%Y-%m-%d'),
        date_to=datetime.strptime(date_to, '%Y-%m-%d')
    )

    if hotels:
        print(hotels[0].values())
    else:
        assert hotels == []
        print(f'No hotels')



@pytest.mark.parametrize('hotel_id,date_from,date_to',[
    (1, '2023-06-10', '2023-06-20'),
    (33, '2023-06-10', '2023-06-20'),
])
async def test_search_for_rooms(hotel_id, date_from, date_to):
    rooms = await RoomsDAO.search_for_rooms(
        hotel_id,
        date_from=datetime.strptime(date_from, '%Y-%m-%d'),
        date_to=datetime.strptime(date_to, '%Y-%m-%d')
    )

    if rooms:
        print(f'Name of the room is {rooms[0].name}')
    else:
        assert rooms == []
        print(f'No rooms')


