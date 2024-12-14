from pydantic import BaseModel, Field


class ProductCreate(BaseModel):
    title: str
    price: int = Field(ge=0)
    amount: int = Field(ge=0)
    description: str


class ProductResponse(ProductCreate):
    id: int
    seller_id: int