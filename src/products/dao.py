from fastapi.encoders import jsonable_encoder
from sqlalchemy import update, delete
from src.dao import BaseDAO
from src.exceptions import NoPermissionsException, NotFoundException
from src.products import Product
from src.database import async_session


class ProductDAO(BaseDAO):
    """
    Data Access Object to work with Product models.
    """

    model = Product

    @classmethod
    async def add(cls, title: str, price: int, amount: int, description: str, seller_id: int) -> Product:
        """
        Adds product to database.

        :param title: Title of product.
        :param price: Price of product.
        :param amount: Amount of product.
        :param description: Description of product.
        :param seller_id: Id of user who sells it.
        :return: Nothing.
        """

        async with async_session() as session:
            async with session.begin():
                new_product = Product(title=title, price=price, amount=amount,
                                    description=description, seller_id=seller_id)
                session.add(new_product)
                await session.flush()
                return jsonable_encoder(new_product)

    @classmethod
    async def edit(cls, product_id: int, **values) -> Product:
        """
        Changes necessary fields of product.

        :param product_id: Id of product you want to change.
        :param values: Fields that you want to change.
        :return: Changed product.
        """

        async with async_session() as session:
            async with session.begin():
                stmt = (
                    update(cls.model).
                    filter_by(id=product_id).
                    values(**values).
                    returning(cls.model.id)
                )
                changed_product_id = await session.execute(stmt)
                return changed_product_id.scalar()

    @classmethod
    async def delete(cls, product_id: int, user_id: int):
        """
        Deletes the product.

        :param product_id: Id of product
        :param user_id: Id of user
        :return: Nothing.
        """
        async with async_session() as session:
            async with session.begin():
                stmt = (
                    delete(cls.model).
                    filter_by(id=product_id).
                    returning(cls.model)
                )
                deleted_product = await session.execute(stmt)
                deleted_product = deleted_product.scalar()
                if deleted_product is None:
                    raise NotFoundException
                if deleted_product.seller_id != user_id:
                    raise NoPermissionsException