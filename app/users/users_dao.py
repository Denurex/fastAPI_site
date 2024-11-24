from app.dao.base import BaseDAO
from app.users.users_models import Users


class UsersDAO(BaseDAO):
    model = Users
