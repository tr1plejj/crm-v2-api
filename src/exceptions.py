from fastapi import HTTPException, status

NoPermissionsException = HTTPException(
    detail='You have no permissions to do that',
    status_code=status.HTTP_403_FORBIDDEN
)

NotFoundException = HTTPException(
    detail='Item not found',
    status_code=status.HTTP_400_BAD_REQUEST
)