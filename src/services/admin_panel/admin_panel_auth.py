from fastapi import HTTPException, Depends
from sqladmin.authentication import AuthenticationBackend
from sqlalchemy import select
from starlette import status
from starlette.requests import Request
from starlette.responses import RedirectResponse

from src.conf.messages import AuthMessages
from src.database.db import get_db, sessionmanager
from src.database.models import User
from src.repository import users as repository_users
from src.services.auth import auth_service


class AdminAuth(AuthenticationBackend):
    async def login(self, request: Request) -> bool:
        form = await request.form()
        email, password = form["username"], form["password"]

        async with sessionmanager.session() as session:
            sq = select(User).filter_by(email=email)
            result = await session.execute(sq)
            user = result.scalar_one_or_none()

        if user is None:
            raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail=AuthMessages.invalid_email)
        if not user.confirmed:
            raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail=AuthMessages.email_not_confirmed)
        if not auth_service.verify_password(password, user.password):
            raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail=AuthMessages.invalid_password)
        if user.banned:
            raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail=AuthMessages.banned)

        access_token = await auth_service.create_access_token(data={"sub": user.email})
        request.session.update({"token": access_token})

        return True

    async def logout(self, request: Request) -> bool:
        request.session.clear()
        return True

    async def authenticate(self, request: Request) -> bool:
        token = request.session.get("token")

        if not token:
            return False

        user = Depends(auth_service.get_current_user)
        if not user:
            return False

        return True


authentication_backend = AdminAuth(secret_key="...")
