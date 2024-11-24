from datetime import date
from typing import Optional

from pydantic import BaseModel, EmailStr


class SUserRegisterAndAuth(BaseModel):
    email: EmailStr
    password: str

    class Config:
        orm_mode = True
