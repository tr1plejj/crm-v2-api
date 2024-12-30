from typing import Annotated
from fastapi import APIRouter, Depends, UploadFile
from fastapi.params import Path, File, Form
from pathlib import Path as FilePath
from fastapi.responses import FileResponse
from redis_tools import RedisTools
from src.auth import User
from src.auth.config import current_active_user
from src.exceptions import NoPermissionsException
from src.products.dao import ProductDAO
from src.products.schemas import ProductResponse
from .exceptions import ImageNotFoundException, NotAPictureException

router = APIRouter(
    prefix='/products',
    tags=['products']
)

UPLOAD_FOLDER = FilePath('images')

@router.post('/', status_code=201, response_model=ProductResponse)
async def create_product(
        file: Annotated[UploadFile, File(description='An image for your product')],
        title: Annotated[str, Form()],
        price: Annotated[int, Form(ge=0)],
        amount: Annotated[int, Form(ge=0)],
        description: Annotated[str, Form()],
        user: User = Depends(current_active_user)
):
    new_product = await ProductDAO.add(title, price, amount, description, user.id)
    if file.content_type == 'image/jpeg':
        filetype = 'jpg'
    elif file.content_type == 'image/png':
        filetype = 'png'
    else:
        raise NotAPictureException
    file_location = UPLOAD_FOLDER / f'{new_product['id']}.{filetype}'
    with open(file_location, "wb") as file_object:
        content = await file.read()
        file_object.write(content)
    return new_product


@router.get('/', response_model=list[ProductResponse])
async def list_products():
    products = await ProductDAO.find_all()
    return products


@router.get('/{product_id}', response_model=ProductResponse)
async def get_product(product_id: Annotated[int, Path()]):
    product = RedisTools.get_product(product_id=product_id)
    if not product:
        product = await ProductDAO.find_one_or_none(id=product_id)
        RedisTools.set_product(product_id, product)
    return product


@router.get('/image/{product_id}')
def get_product_image(product_id: Annotated[int, Path()]): # -> make path returning instead of image itself
    file_location = UPLOAD_FOLDER / f'{product_id}.png'
    if file_location.exists():
        return FileResponse(file_location)
    file_location = UPLOAD_FOLDER / f'{product_id}.jpg'
    if file_location.exists():
        return FileResponse(file_location)
    raise ImageNotFoundException


@router.patch('/{product_id}')
async def edit_product(
        product_id: Annotated[int, Path()],
        price: Annotated[int, Form()] = None,
        amount: Annotated[int, Form()] = None,
        description: Annotated[str, Form()] = None,
        user: User = Depends(current_active_user)
):
    product = await ProductDAO.find_one_or_none(id=product_id)
    if product.seller_id != user.id:
        raise NoPermissionsException
    product_amount = product.amount
    product_price = product.price
    product_description = product.description

    if description:
        product_description = description
    if price:
        product_price = price
    if amount:
        product_amount = amount

    changed_product_id = await ProductDAO.edit(
        product_id=product_id,
        description=product_description,
        amount=product_amount,
        price=product_price
    )
    return {'changed_product_id': changed_product_id}


@router.delete('/{product_id}')
async def delete_product(product_id: Annotated[int, Path()], user: User = Depends(current_active_user)):
    await ProductDAO.delete(product_id=product_id, user_id=user.id)
    return {'data': f'product {product_id} deleted successfully'}


