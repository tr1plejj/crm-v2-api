from pydantic import BaseModel


class ProductSchema(BaseModel):
    title: str
    quantity: int
    price: int
    description: str


class ProductSchemaInDB(ProductSchema):
    id: int

