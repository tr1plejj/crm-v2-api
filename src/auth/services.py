from typing import Annotated
from fastapi import Depends
from fastapi.encoders import jsonable_encoder
from datetime import datetime, UTC, timedelta

from sqlalchemy.orm import selectinload

from src.auth.exceptions import credentials_error
from jwt import InvalidTokenError
from src.auth.config import pwd_context
from database import async_session
from models import UserOrm
from sqlalchemy import select
from src.auth.schemas import UserSchemaInDB, TokenData
import jwt
from src.auth.config import SECRET_KEY, ALGORITHM, oauth2_scheme


def verify_password(password, hashed_password):
    return pwd_context.verify(password, hashed_password)


def hash_password(password):
    return pwd_context.hash(password)


async def get_user(username: str):
    async with async_session() as session:
        query = (
            select(UserOrm).filter_by(username=username)
            .options(selectinload(UserOrm.products))
        )
        user = await session.execute(query)
        user = user.scalars().one()
    user = jsonable_encoder(user)
    return UserSchemaInDB(**user)


async def authenticate_user(username: str, password: str):
    user = await get_user(username)
    if not user:
        return False
    if not verify_password(password, user.hashed_password):
        return False
    return user


async def create_jwt(data: dict, expires_delta: timedelta | None = None):
    to_encode = data.copy()
    if expires_delta:
        expire = datetime.now(UTC) + expires_delta
    else:
        expire = datetime.now(UTC) + timedelta(minutes=60)
    to_encode.update({'exp': expire})
    encoded_jwt = jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)
    return encoded_jwt


async def get_current_user(token: Annotated[str, Depends(oauth2_scheme)]):
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        username: str = payload.get('sub')
        if username is None:
            raise credentials_error
        token_data = TokenData(username=username)
    except InvalidTokenError:
        raise credentials_error
    user = await get_user(token_data.username)
    if user is None:
        raise credentials_error
    return user