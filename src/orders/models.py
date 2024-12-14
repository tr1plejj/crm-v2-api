from sqlalchemy import Integer, ForeignKey, String
from sqlalchemy.orm import Mapped, mapped_column, relationship
from src import Base, User


class Order(Base):
    __tablename__ = 'order'

    id: Mapped[int] = mapped_column(
        Integer, primary_key=True
    )
    buyer_id: Mapped[int] = mapped_column(
        Integer, nullable=False
    )
    seller_id: Mapped[int] = mapped_column(
        Integer, ForeignKey('user.id'), nullable=False
    )
    city: Mapped[str] = mapped_column(
        String, nullable=False
    )
    address: Mapped[str] = mapped_column(
        String, nullable=False
    )
    index: Mapped[int] = mapped_column(
        Integer, nullable=False
    )
    seller: Mapped['User'] = relationship(
        'User', back_populates='orders'
    )
    product_id: Mapped[int] = mapped_column(
        Integer, ForeignKey('product.id'), nullable=False
    )
    amount: Mapped[int] = mapped_column(
        Integer, nullable=False
    )

User.orders = relationship('Order', back_populates='seller')