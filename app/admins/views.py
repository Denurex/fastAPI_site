from sqladmin import ModelView

from app.bookings.models import Bookings
from app.hotels.models import Hotels, Rooms
from app.users.users_models import Users


class UserAdmin(ModelView, model=Users):
    can_delete = False
    can_edit = False
    name = 'Пользователь'
    name_plural = 'Пользователи'
    icon = "fa-solid fa-user"
    # category = "Аккаунт"
    column_list = [Users.id, Users.email]
    column_details_list = [Users.id, Users.email, Users.booking]
    # column_formatters = None


class BookingsAdmin(ModelView, model=Bookings):
    can_delete = False
    can_edit = False
    name = 'Бронь'
    name_plural = 'Брони'
    icon = "fa-solid fa-user"
    # category = "Бронирование"

    column_list = "__all__"
    #or
    # column_list = [c.name for c in Bookings.__table__.c]


class RoomsAdmin(ModelView, model=Rooms):
    can_delete = False
    can_edit = False
    name = 'Комната'
    name_plural = 'Комнаты'
    icon = "fa-solid fa-bed"
    column_list = "__all__"


class HotelsAdmin(ModelView, model=Hotels):
    can_delete = False
    can_edit = False
    name = 'Отель'
    name_plural = 'Отели'
    icon = "fa-solid fa-hotel"
    column_list = "__all__"



