from sqlalchemy import ForeignKey
from sqlalchemy.orm import Mapped, mapped_column, relationship, DeclarativeBase


class Base(DeclarativeBase):
    pass


class UserOrm(Base):
    __tablename__ = 'user'
    id: Mapped[int] = mapped_column(primary_key=True)
    username: Mapped[str] = mapped_column(unique=True)
    email: Mapped[str]
    name: Mapped[str]
    surname: Mapped[str]
    phone_number: Mapped[int]
    hashed_password: Mapped[str]
    products: Mapped[list['ProductOrm']] = relationship(
        back_populates="user",
        primaryjoin="UserOrm.id == ProductOrm.user_id",
    )


class ProductOrm(Base):
    __tablename__ = 'product'
    id: Mapped[int] = mapped_column(primary_key=True)
    title: Mapped[str]
    quantity: Mapped[int]
    price: Mapped[int]
    description: Mapped[str]
    user_id: Mapped[int] = mapped_column(ForeignKey('user.id', ondelete='CASCADE'))
    user: Mapped['UserOrm'] = relationship(back_populates='products')