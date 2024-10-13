from typing import Annotated
from sqlalchemy import select, update, delete
from src.auth.schemas import UserSchema
from fastapi import APIRouter, Depends, Query, Path
from fastapi.encoders import jsonable_encoder
from src.auth.services import get_current_user
from src.crm.schemas import ProductSchema, ProductSchemaInDB
from models import ProductOrm
from database import async_session
from fastapi_cache.decorator import cache

router = APIRouter(tags=['products'])


@router.post('/create/', response_model=ProductSchemaInDB)
async def create_product(current_user: Annotated[UserSchema, Depends(get_current_user)], product: ProductSchema):
    async with async_session() as session:
        new_product = ProductOrm(**product.model_dump(), user_id=current_user.id)
        session.add(new_product)
        await session.commit()
        await session.refresh(new_product)
    return ProductSchemaInDB(**jsonable_encoder(new_product))


@router.get('/product/{product_id}', response_model=ProductSchemaInDB)
@cache(expire=60)
async def get_product(product_id: Annotated[int, Path()]):
    async with async_session() as session:
        query = (
            select(ProductOrm).
            filter_by(id=product_id)
        )
        product = await session.execute(query)
    product = product.scalar()
    return ProductSchemaInDB(**jsonable_encoder(product))


@router.patch('/product/{product_id}')
async def update_product(product_id: Annotated[int, Path()], quantity: Annotated[int, Query()]) -> dict[str, int]:
    async with async_session() as session:
        query = (
            select(ProductOrm.quantity).
            filter_by(id=product_id)
        )
        current_quantity = await session.execute(query)
        current_quantity = current_quantity.one()[0]
        new_quantity = current_quantity + quantity
        stmt = (
            update(ProductOrm).
            where(ProductOrm.id == product_id).
            values(quantity=new_quantity).
            returning(ProductOrm.quantity)
        )
        product = await session.execute(stmt)
        await session.commit()
    return {'product_id': product_id, 'new_quantity': product.scalar()}


@router.delete('/product/{product_id}')
async def delete_product(product_id: Annotated[int, Path()]):
    async with async_session() as session:
        stmt = (
            delete(ProductOrm).
            where(ProductOrm.id == product_id)
        )
        await session.execute(stmt)
        await session.commit()
    return {'status': 200}