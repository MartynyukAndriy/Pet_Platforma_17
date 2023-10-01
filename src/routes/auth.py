import re

from fastapi import APIRouter, HTTPException, Depends, status, Security, BackgroundTasks, Request
from fastapi.security import OAuth2PasswordRequestForm, HTTPAuthorizationCredentials, HTTPBearer
from sqlalchemy.ext.asyncio import AsyncSession

from src.database.db import get_db
from src.repository import users as repository_users
from src.repository import masters as repository_masters
from src.schemas.user_schemas import UserModel, UserRes, MasterResponse, MasterModel
from src.schemas.auth_schemas import TokenModel, RequestEmail
from src.services.auth import auth_service
from src.services.email import send_email
from src.conf.messages import AuthMessages

router = APIRouter(prefix='/auth', tags=["auth"])
security = HTTPBearer()


async def validate_pwd(password: str) -> str|bool:
        pwd_pattern = r"((?=.*d)(?=.*[a-z])(?=.*[A-Z]).{8,})"
        if re.match(pwd_pattern, password):
            return password
        else:
            return False

    #
    # #  (                Начало группы
    # #  (?=.*d)          Должен содержать цифру от 0 до 9
    # #  (?=.*[a-z])      Должен содержать символ латинницы в нижем регистре
    # #  (?=.*[A-Z])      Должен содержать символ латинницы в верхнем регистре
    # #  (?=.*[@#$%])     Должен содержать специальный символ из списка "@#$%"
    # #  .                Совпадает с предыдущими условиями
    # #  {8,20}           Длина - от 8 до 20 символов
    # #  )                Конец группы


@router.post("/signup_user", response_model=UserRes|str, status_code=status.HTTP_201_CREATED)
async def signup_user(body: UserModel,
                      background_tasks: BackgroundTasks,
                      request: Request,
                      db: AsyncSession = Depends(get_db)):

    exist_user = await repository_users.get_user_by_email(body.email, db)
    if exist_user:
        raise HTTPException(status_code=status.HTTP_409_CONFLICT, detail=AuthMessages.account_already_exists)

    is_true_password = await validate_pwd(body.password)
    if is_true_password:
        body.password = auth_service.get_password_hash(body.password)
        new_user = await repository_users.create_user(body, db)
        background_tasks.add_task(send_email, new_user.email, new_user.name, str(request.base_url))
        return new_user
    else:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN,
                            detail="Password doesn't match requiments. The password must be at least 8 characters, contain lowercase and uppercase letters and numbers!")


@router.post("/signup_master", response_model=MasterResponse, status_code=status.HTTP_201_CREATED)
async def signup_master(body: MasterModel,
                        background_tasks: BackgroundTasks,
                        request: Request,
                        db: AsyncSession = Depends(get_db)):
    exist_user = await repository_users.get_user_by_email(body.email, db)
    if exist_user:
        raise HTTPException(status_code=status.HTTP_409_CONFLICT, detail=AuthMessages.account_already_exists)

    is_true_password = await validate_pwd(body.password)
    if is_true_password:
        body.password = auth_service.get_password_hash(body.password)
        new_master = await repository_masters.create_master(body, db)
        background_tasks.add_task(send_email, body.email, body.name, str(request.base_url))
        return new_master
    else:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="Password doesn't match requiments. The password must be at least 8 characters, contain lowercase and uppercase letters and numbers!")


@router.post("/login", response_model=TokenModel)
async def login(body: OAuth2PasswordRequestForm = Depends(), db: AsyncSession = Depends(get_db)):

    user = await repository_users.get_user_by_email(body.username, db)
    if user is None:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail=AuthMessages.invalid_email)
    if not user.confirmed:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail=AuthMessages.email_not_confirmed)
    if not auth_service.verify_password(body.password, user.password):
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail=AuthMessages.invalid_password)
    if user.banned:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail=AuthMessages.banned)
    # Generate JWT
    access_token = await auth_service.create_access_token(data={"sub": user.email})
    refresh_token = await auth_service.create_refresh_token(data={"sub": user.email})
    await repository_users.update_token(user, refresh_token, db)
    return {"access_token": access_token, "refresh_token": refresh_token, "token_type": "bearer"}


@router.get('/refresh_token', response_model=TokenModel)
async def refresh_token(credentials: HTTPAuthorizationCredentials = Security(security),
                        db: AsyncSession = Depends(get_db)):

    token = credentials.credentials
    email = await auth_service.decode_refresh_token(token)
    user = await repository_users.get_user_by_email(email, db)
    if user.refresh_token != token:
        await repository_users.update_token(user, None, db)
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail=AuthMessages.invalid_refresh_token)
    if user.banned:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail=AuthMessages.banned)

    access_token = await auth_service.create_access_token(data={"sub": email})
    refresh_token = await auth_service.create_refresh_token(data={"sub": email})
    await repository_users.update_token(user, refresh_token, db)
    return {"access_token": access_token, "refresh_token": refresh_token, "token_type": "bearer"}


@router.get('/confirmed_email/{token}')
async def confirmed_email(token: str, db: AsyncSession = Depends(get_db)):

    email = await auth_service.get_email_from_token(token)
    user = await repository_users.get_user_by_email(email, db)
    if user is None:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=AuthMessages.verification_error)
    if user.confirmed:
        return {"message": "Your email is already confirmed"}
    await repository_users.confirmed_email(email, db)
    return {"message": "Email confirmed"}


@router.post('/request_email')
async def request_email(body: RequestEmail, background_tasks: BackgroundTasks, request: Request,
                        db: AsyncSession = Depends(get_db)):
    user = await repository_users.get_user_by_email(body.email, db)
    if user.confirmed:
        return {"message": AuthMessages.your_email_is_already_confirmed}
    if user:
        background_tasks.add_task(send_email, user.email, user.name, str(request.base_url))
    return {"message": AuthMessages.check_your_email_for_confirmation}
