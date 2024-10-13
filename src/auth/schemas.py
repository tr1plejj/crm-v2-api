from pydantic import BaseModel, EmailStr

from src.crm.schemas import ProductSchemaInDB


class UserSchema(BaseModel):
    username: str
    email: EmailStr
    name: str
    surname: str
    phone_number: int


class NewUserSchema(UserSchema):
    hashed_password: str


class UserSchemaInDB(NewUserSchema):
    id: int
    products: list[ProductSchemaInDB]


class Token(BaseModel):
    access_token: str
    token_type: str


class TokenData(BaseModel):
    username: str
