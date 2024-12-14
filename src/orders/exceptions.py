from fastapi import HTTPException, status

NotEnoughAmountException = HTTPException(
    status_code=status.HTTP_400_BAD_REQUEST,
    detail='Запрошенное количество превышает имеющееся у продукта'
)