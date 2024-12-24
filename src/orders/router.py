from typing import Annotated
from fastapi import APIRouter, Depends
from fastapi.params import Path
from redis_tools import RedisTools
from src.auth import User
from src.auth.config import current_active_user
from src.orders.dao import OrderDAO
from src.orders.schemas import OrderResponse, OrderCreate

router = APIRouter(
    tags=['orders'],
    prefix='/orders'
)


@router.post('/create/', response_model=OrderResponse, status_code=201)
async def create_order(order: OrderCreate):
    new_order = await OrderDAO.create(
        buyer_id=order.buyer_id,
        seller_id=order.seller_id,
        product_id=order.product_id,
        amount=order.amount,
        city=order.city,
        address=order.address,
        index=order.index
    )
    return new_order


@router.get('/', response_model=list[OrderResponse])
async def list_orders():
    orders = await OrderDAO.find_all()
    return orders


@router.delete('/{order_id}/')
async def delete_order(order_id: Annotated[int, Path()], user: User = Depends(current_active_user)):
    deleted_order = await OrderDAO.remove(order_id=order_id, seller_id=user.id)
    return deleted_order


@router.get('/{order_id}/', response_model=OrderResponse)
async def get_order(order_id: Annotated[int, Path()]):
    order = RedisTools.get_order(order_id=order_id)
    if not order:
        order = await OrderDAO.find_one_or_none(id=order_id)
        RedisTools.set_order(order_id=order_id, order_obj=order)
    return order