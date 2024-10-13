from datetime import timedelta
from typing import Annotated
from fastapi.security import OAuth2PasswordRequestForm
from fastapi import APIRouter, Depends
from sqlalchemy.exc import IntegrityError
from database import async_session
from src.auth.exceptions import incorrect_data, not_unique
from models import UserOrm
from src.auth.schemas import Token, UserSchema, NewUserSchema, UserSchemaInDB
from src.auth.services import authenticate_user, create_jwt, get_current_user, hash_password
from src.auth.config import TOKEN_EXPIRES_MINUTES

router = APIRouter(tags=['auth'])


@router.post('/token')
async def login(form_data: Annotated[OAuth2PasswordRequestForm, Depends()]) -> Token:
    user = await authenticate_user(form_data.username, form_data.password)
    if not user:
        raise incorrect_data
    access_token_expires = timedelta(TOKEN_EXPIRES_MINUTES)
    access_token = await create_jwt({'sub': user.username}, access_token_expires)
    return Token(access_token=access_token, token_type='bearer')


@router.get('/users/me', response_model=UserSchemaInDB)
async def get_current_user(current_user: Annotated[UserSchema, Depends(get_current_user)]):
    return current_user


@router.post('/register')
async def register(new_user: NewUserSchema):
    try:
        async with async_session() as session:
            hashed_password = hash_password(new_user.hashed_password)
            user = UserOrm(username=new_user.username, hashed_password=hashed_password,
                           email=new_user.email, name=new_user.name, surname=new_user.surname,
                           phone_number=new_user.phone_number)
            session.add(user)
            await session.commit()
        return UserSchema(**new_user.model_dump())
    except IntegrityError:
        raise not_unique

