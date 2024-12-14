from fastapi.encoders import jsonable_encoder
from sqlalchemy import select, update, delete

from src.exceptions import NoPermissionsException, NotFoundException
from src.orders import Order
from src.orders.exceptions import NotEnoughAmountException
from src.products import Product
from src.dao import BaseDAO
from src.database import async_session


class OrderDAO(BaseDAO):
    """
    Data Access Object to work with Order models.
    """
    model = Order

    @classmethod
    async def create(
            cls,
            buyer_id: int,
            seller_id: int,
            product_id: int,
            amount: int,
            city: str,
            address: str,
            index: int
    ) -> Order:
        """
        Create order. Automatically changes amount for -1.

        :param buyer_id: Id of buyer.
        :param seller_id: Id of seller.
        :param product_id: Id of product.
        :param amount: Available amount of product.
        :param city: Buyer's city.
        :param address: Buyer's address.
        :param index: Buyer's index.
        :return: Created object of Order.
        """

        async with async_session() as session:
            async with session.begin():
                amount_query = select(Product.amount).filter_by(id=product_id)
                product_amount = await session.execute(amount_query)
                if product_amount is None:
                    raise NotFoundException
                new_amount = product_amount.scalar() - amount
                if new_amount < 0:
                    raise NotEnoughAmountException
                stmt = (
                    update(Product).
                    filter_by(id=product_id).
                    values(amount=new_amount)
                )
                await session.execute(stmt)
                new_order = Order(
                    buyer_id=buyer_id,
                    seller_id=seller_id,
                    product_id=product_id,
                    amount=amount,
                    city=city,
                    address=address,
                    index=index
                )
                session.add(new_order)
                await session.flush()
                return jsonable_encoder(new_order)

    @classmethod
    async def remove(cls, order_id: int, seller_id: int) -> Order:
        """
        Remove the order. Automatically checks is user the seller.

        :param order_id: Id of order.
        :param seller_id: Id of seller.
        :return: Deleted object of Order.
        """

        async with async_session() as session:
            async with session.begin():
                stmt = (
                    delete(cls.model).
                    filter_by(id=order_id).
                    returning(cls.model)
                )
                order = await session.execute(stmt)
                order = order.scalar()
                if order is None:
                    raise NotFoundException
                if order.seller_id != seller_id:
                    raise NoPermissionsException

                return jsonable_encoder(order)