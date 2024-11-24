from datetime import datetime

from fastapi import Request
from fastapi.params import Depends
from jose import JWTError, jwt

from app.config import settings
from app.exceptions import *
from app.users.users_dao import UsersDAO


def get_token(request: Request):
    token = request.cookies.get('booking_access_token')
    if not token:
        raise TokenIsNoneException
    return token


async def get_current_user(token: str = Depends(get_token)):
    # print(jwt.decode(token, settings.SECRET_KEY, settings.ALGORITHM))
    try:
        jwt_decode = jwt.decode(token, settings.SECRET_KEY, settings.ALGORITHM)
    except JWTError:
        raise DecodeException

    expire: int = jwt_decode.get('exp')
    if expire < int(datetime.utcnow().timestamp()):
        raise TokenExpireDateException

    user_id = jwt_decode.get('sub')
    if not user_id:
        raise UseridException

    user = await UsersDAO.find_by_id(int(user_id))
    if not user:
        raise UserException
    return user
