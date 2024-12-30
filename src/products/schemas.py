from pydantic import BaseModel, Field


class ProductResponse(BaseModel):
    id: int
    seller_id: int
    title: str
    price: int = Field(ge=0)
    amount: int = Field(ge=0)
    description: str
    image: str
