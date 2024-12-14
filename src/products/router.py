from typing import Annotated
from fastapi import APIRouter, Depends
from fastapi.params import Path, Query

from redis_tools import RedisTools
from src.auth import User
from src.auth.config import current_active_user
from src.exceptions import NoPermissionsException
from src.products.dao import ProductDAO
from src.products.schemas import ProductCreate, ProductResponse

router = APIRouter(
    prefix='/products',
    tags=['products']
)


@router.post('/')
async def create_product(product: ProductCreate, user: User = Depends(current_active_user)):
    new_product = await ProductDAO.add(product.title, product.price, product.amount, product.description, seller_id=user.id)
    return new_product


@router.get('/', response_model=list[ProductResponse])
async def list_products():
    products = await ProductDAO.find_all()
    return products


@router.get('/{product_id}/', response_model=ProductResponse)
async def get_product(product_id: Annotated[int, Path()]):
    product = RedisTools.get_product(product_id=product_id)
    if not product:
        product = await ProductDAO.find_one_or_none(id=product_id)
        RedisTools.set_product(product_id, product)
    return product


@router.patch('/{product_id}/')
async def edit_product(
        product_id: Annotated[int, Path()],
        price: Annotated[int, Query()] = None,
        amount: Annotated[int, Query()] = None,
        description: Annotated[str, Query()] = None,
        user: User = Depends(current_active_user)
):
    product = await ProductDAO.find_one_or_none(id=product_id)
    if product.seller_id != user.id:
        raise NoPermissionsException
    product_amount = product.amount
    product_price = product.price
    product_description = product.description

    if description:
        product_description = description
    if price:
        product_price = price
    if amount:
        product_amount = amount

    changed_product_id = await ProductDAO.edit(
        product_id=product_id,
        description=product_description,
        amount=product_amount,
        price=product_price
    )
    return {'changed_product_id': changed_product_id}


@router.delete('/{product_id}/')
async def delete_product(product_id: Annotated[int, Path()], user: User = Depends(current_active_user)):
    deleted_product = await ProductDAO.delete(product_id=product_id, user_id=user.id)
    return deleted_product


