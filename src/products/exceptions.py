from fastapi import HTTPException

NotAPictureException = HTTPException(
    status_code=403,
    detail='This is not a picture (.jpg and .png only)'
)