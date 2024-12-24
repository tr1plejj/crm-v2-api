from fastapi import HTTPException

ImageNotFoundException = HTTPException(
    status_code=404,
    detail='Image with that id not found'
)

NotAPictureException = HTTPException(
    status_code=403,
    detail='This is not a picture (.jpg and .png only)'
)