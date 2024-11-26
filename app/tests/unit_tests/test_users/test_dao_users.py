import pytest

from app.users.users_dao import UsersDAO


@pytest.mark.parametrize('user_id,email, is_exists',[
    (1, 'fedor@moloko.ru', True),
    (10, 'aaaaa@moloko.ru', False),

])
async def test_find_by_id(user_id, email, is_exists):
    user = await UsersDAO.find_by_id(user_id)
    print(user)
    if is_exists:
        assert user
        assert user.id == user_id
        assert user.email == email
    else:
        assert user is None
