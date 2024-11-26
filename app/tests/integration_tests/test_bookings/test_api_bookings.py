import pytest
from httpx import AsyncClient


@pytest.mark.parametrize('room_id,date_from,date_to,status_code', [
    *[(1, '2023-06-20', '2023-07-10', 200)]*2,
    (1, '2023-06-20', '2023-07-10', 409)
])
async def test_add_booking(room_id, date_from, date_to, status_code, authenticated_ac: AsyncClient):
    response = await authenticated_ac.post('/bookings/add_booking', params={
        "room_id": room_id,
        "date_from": date_from,
        "date_to": date_to
    })

    assert response.status_code == status_code


async def test_get_booking(authenticated_ac: AsyncClient):
    response = await authenticated_ac.get('/bookings')

    print(response.json()[0].values())
    assert response.status_code == 200
