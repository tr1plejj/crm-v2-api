from pydantic import BaseModel, Field


class OrderCreate(BaseModel):
    buyer_id: int
    seller_id: int
    product_id: int
    amount: int = Field(gt=0)
    city: str
    address: str
    index: int

class OrderResponse(OrderCreate):
    id: int