from fastapi import APIRouter, Depends, Response

from app.exceptions import *
from app.users.users_auth import (authenticate_user, create_access_token,
                                  get_password_hash, verify_password)
from app.users.users_dao import UsersDAO
from app.users.users_dependencies import get_current_user
from app.users.users_models import Users
from app.users.users_shemas import SUserRegisterAndAuth

router = APIRouter(prefix='/auth',
                   tags=['Регистрация'])


@router.post('/register')
async def register_user(user_data: SUserRegisterAndAuth):
    existing_user = await UsersDAO.find_one_or_none(email=user_data.email)
    if existing_user:
        raise UserAlreadyExists
    hashed_password = get_password_hash(user_data.password)
    await UsersDAO.add_new(email=user_data.email, password=hashed_password)


@router.post('/login')
async def login_user(response: Response, user_data: SUserRegisterAndAuth):
    user = await authenticate_user(user_data.email, user_data.password)
    if not user:
        raise IncorrectEmailOrPassword
    access_token = create_access_token({'sub': str(user.id)})
    response.set_cookie('booking_access_token', access_token, httponly=True)
    return access_token


@router.post('/logout')
def logout_user(response: Response):
    response.delete_cookie('booking_access_token')


@router.get('/profile')
async def check_profile(user: Users = Depends(get_current_user)):
    return user