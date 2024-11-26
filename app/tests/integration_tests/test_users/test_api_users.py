import pytest
from httpx import AsyncClient


@pytest.mark.parametrize('email,password,status_code',[
    ('testtt@example.com','testt', 200),
    ('testtt@example.com','testt111', 409),
    ('sdfgsdf@example.com','testt111', 200),
    ('aaaaaaaaaaa.com', 'testt111', 422),

])
async def test_register_user(email, password, status_code, ac: AsyncClient):
    response = await ac.post('/auth/register', json={
        'email':email,
        'password':password
    })

    assert response.status_code == status_code


@pytest.mark.parametrize('email,password,status_code',[
    ('user@example.com','string', 200),
    ('kjklj@example.com','testt111', 401),

])
async def test_login_user(email, password, status_code, ac: AsyncClient):
    response = await ac.post('/auth/login', json={
        'email':email,
        'password':password
    })

    assert response.status_code == status_code