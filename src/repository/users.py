from fastapi import HTTPException
from sqlalchemy import select
from sqlalchemy.orm import Session
from starlette import status

from src.database.models import User, Admin, MasterInfo
from src.schemas.user_schemas import UserModel, MasterModel, AdminModel, UserUpdate, UserBlackList


async def get_user_by_email(email: str, db: Session) -> User | None:
    """
    The get_user_by_email function takes in an email and a database session,
    and returns the user associated with that email. If no such user exists, it returns None.

    :param email: str: Pass the email address of the user to be retrieved
    :param db: Session: Pass in a database session
    :return: A user object or none
    """
    return select(User).filter(User.email == email)


async def create_user(body: UserModel, db: Session) -> User:
    """
    The create_user function creates a new user in the database.
        If there are no users with admin role, then the new user will be created as an admin.
        Otherwise, it will be created as a regular user.

    :param body: UserModel: Create a new user object
    :param db: Session: Access the database
    :return: A user object
    """
    admin_exists = select(User).filter(User.role == 'superadmin')
    print(admin_exists)

    if not admin_exists:
        new_user = User(**body.model_dump())
        new_user.user_role = 'superadmin'
        db.add(new_user)

        created_user = await get_user_by_email(new_user.email, db)
        new_admin = Admin(user_id=created_user.user_id, is_active=True)
        db.add(new_admin)

        await db.commit()
        await db.refresh(new_user)
        await db.refresh(new_admin)

        return new_user

    elif body.user_role == "client":
        new_user = User(**body.model_dump())
        db.add(new_user)
        await db.commit()
        await db.refresh(new_user)

        return new_user

    elif body.user_role == "master":
        body = MasterModel
        new_user = User(
            user_role='master',
            password=body.password,
            name=body.name,
            email=body.email,
            country_id=body.country_id,
            city_id=body.city_id,
            phone=body.phone,
            avatar=body.avatar,
        )
        db.add(new_user)

        created_user = await get_user_by_email(new_user.email, db)
        new_master = MasterInfo(
            user_id=created_user.user_id,
            description=body.description,
            salon_name=body.name,
            salon_address=body.salon_address,
            longitude=body.longitude,
            latitude=body.latitude,
            is_active=body.is_active,
        )
        db.add(new_master)

        await db.commit()
        await db.refresh(new_user)
        await db.refresh(new_master)

        return new_user


async def update_token(user: User, token: str | None, db: Session) -> None:
    """
    The update_token function updates the refresh token for a user.

    :param user: User: Identify the user that is being updated
    :param token: str | None: Pass in the token that is returned from the api
    :param db: Session: Access the database
    :return: Nothing
    """
    user.refresh_token = token
    await db.commit()


async def confirmed_email(email: str, db: Session) -> None:
    """
    The confirmed_email function takes in an email and a database session,
    and sets the confirmed field of the user with that email to True.

    :param email: str: Pass the email of the user to be confirmed
    :param db: Session: Pass the database session to the function
    :return: Nothing
    """
    user = await get_user_by_email(email, db)
    user.confirmed = True
    await db.commit()


async def get_user_info(username: str, db: Session):

    """
    The get_user_info function takes in a username and returns the user's information.
        Args:
            username (str): The name of the user to be retrieved from the database.
    :param username: str: Specify the username of the user
    :param db: Session: Pass the database session to the function
    :return: A dictionary of the user's information
    """
    user = select(User).filter(User.username == username).first()
    return user


async def update_user_info(body: UserUpdate, username: str, db: Session):
    """
    Update the user information with the provided updated fields based on the username.
    :param body: UserUpdate: Updated fields for the user
    :param username: str: User's username
    :param db: Session: Access the database
    :return: Updated user object
    """
    user = db.query(User).filter(User.username == username).first()
    if not user:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="User not found")

    user.username = body.username
    user.email = body.email
    db.commit()
    return user


async def block(email: str, body: UserBlackList, db: Session):
    """Description"""
    user = await get_user_by_email(email, db)
    if user:
        user.banned = body.banned
        db.commit()
    return user
