import pytest
from httpx import AsyncClient


@pytest.mark.parametrize('hotel_id,date_from,date_to,status_code', [
    (1, '2023-06-15', '2023-06-30', 200)
])
async def test_get_rooms_by_date(hotel_id, date_from, date_to, status_code, authenticated_ac: AsyncClient):
    response = await authenticated_ac.get(f'/hotels/{hotel_id}/rooms', params={
        "hotel_id": hotel_id,
        "date_from": date_from,
        "date_to": date_to
    })

    print(response.json()[0])
    assert response.json()[0]['available_rooms'] == 0