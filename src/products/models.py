from sqlalchemy import Integer, String, Text, ForeignKey
from sqlalchemy.orm import Mapped, mapped_column, relationship
from src.database import Base
from src.auth import User


class Product(Base):
    __tablename__ = 'product'

    id: Mapped[int] = mapped_column(
        Integer, primary_key=True
    )
    title: Mapped[str] = mapped_column(
        String(64), index=True, nullable=False
    )
    price: Mapped[int] = mapped_column(
        Integer, nullable=False
    )
    amount: Mapped[int] = mapped_column(
        Integer, nullable=False
    )
    description: Mapped[str] = mapped_column(
        Text, nullable=False
    )
    seller_id: Mapped[int] = mapped_column(
        Integer, ForeignKey('user.id'), nullable=False  # add greater than or equal 0
    )
    seller: Mapped['User'] = relationship(
        'User', back_populates='products'
    )

User.products = relationship('Product', back_populates='seller')