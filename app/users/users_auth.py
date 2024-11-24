from datetime import date, datetime

from asyncpg.pgproto.pgproto import timedelta
from jose import jwt
from passlib.context import CryptContext
from pydantic.v1 import EmailStr

from app.config import settings
from app.users.users_dao import UsersDAO

pwd_context = CryptContext(schemes=['bcrypt'], deprecated='auto')


def get_password_hash(password: str)->str:
    return pwd_context.hash(password)


def verify_password(plain_password, hashed_password)->bool:
    a = pwd_context.verify(plain_password, hashed_password)
    return a


def create_access_token(data: dict)->str:
        to_encode = data.copy()
        expire = datetime.utcnow() + timedelta(minutes=30)
        to_encode.update({'exp': expire})
        encoded_jwt = jwt.encode(to_encode, settings.SECRET_KEY, settings.ALGORITHM)
        return encoded_jwt


async def authenticate_user(email: EmailStr, password: str):
    user = await UsersDAO.find_one_or_none(email=email)
    if not user or not verify_password(password, user.password):
        return None
    return user
