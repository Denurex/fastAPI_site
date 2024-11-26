import pytest
from bookings.dao import BookingDAO
from hotels.hotels_dao import HotelsDAO, RoomsDAO
from users.users_dao import UsersDAO


@pytest.mark.parametrize("dao_class", [
    RoomsDAO, UsersDAO, HotelsDAO, BookingDAO
])
async def test_find_all(dao_class):
    result = await dao_class.find_all()
    print(f'Count of rows {result[0].__tablename__} in db {len(result)}')
    assert isinstance(result, list)



@pytest.mark.parametrize("dao_class,params", [
    (RoomsDAO, {"name": "Делюкс Плюс"}),
    (UsersDAO, {'email':'user@example.com'}),
    (HotelsDAO, {"name": "Ару-Кёль"}),
    (BookingDAO, {"price": 228}),
    (RoomsDAO, {"name": "Делюксссс Плюс"}),
    (UsersDAO, {'email': 'usesdfr@example.com'}),
    (HotelsDAO, {"name": "Ару---Кёль"}),
    (BookingDAO, {"price": 22843})
])
async def test_find_one_or_none(dao_class, params):
    result = await dao_class.find_one_or_none(**params)

    if result is not None:
        print(f'In db in the {result.__tablename__} table, was found entry with params: {params}')
        assert result is not None
    else:
        print(f'In db in the {dao_class.model.__tablename__} table, was --NOT-- found entry with params: {params}')
        assert result is None


@pytest.mark.parametrize("dao_class,id", [
    (RoomsDAO, 1),
    (UsersDAO, 1),
    (HotelsDAO, 1),
    (BookingDAO,1),
    (RoomsDAO, -1),
    (UsersDAO, -1),
    (HotelsDAO, -1),
    (BookingDAO, -1)
])
async def test_find_by_id(dao_class, id):
    result = await dao_class.find_one_or_none(id=id)

    if result is not None:
        print(f'In db in the {result.__tablename__} table, was found entry with id: {id}')
        assert result is not None
    else:
        print(f'In db in the {dao_class.model.__tablename__} table, was --NOT-- found entry with id: {id}')
        assert result is None
