from sqladmin import Admin
from sqladmin.authentication import AuthenticationBackend
from sqlalchemy.testing.suite.test_reflection import users
from starlette.requests import Request
from starlette.responses import RedirectResponse

from app.exceptions import IncorrectEmailOrPassword
from app.users.users_auth import authenticate_user, create_access_token
from app.users.users_dependencies import get_current_user


class AdminAuth(AuthenticationBackend):
    async def login(self, request: Request) -> bool:
        form = await request.form()
        email, password = form["username"], form["password"]
        user = await authenticate_user(email, password)
        if user:
            access_token = create_access_token({'sub': str(user.id)})
            request.session.update({"token": access_token})
        # Validate username/password credentials
        # And update session
        # request.session.update({"token": "..."})

        return True

    async def logout(self, request: Request) -> bool:
        # Usually you'd want to just clear the session
        request.session.clear()
        return True

    async def authenticate(self, request: Request) -> bool:
        token = request.session.get("token")

        if not token:
            return RedirectResponse(request.url_for('admin:login'), status_code=302)

        user = await get_current_user(token)

        if not user or not user.is_admin:
            return RedirectResponse(request.url_for('admin:login'), status_code=302)

        # Check the token in depth
        return True


authentication_backend = AdminAuth(secret_key="...")

