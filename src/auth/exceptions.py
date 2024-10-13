from fastapi import HTTPException

credentials_error = HTTPException(
    detail='Could not validate credentials',
    status_code=401,
    headers={'WWW-Authenticate': 'Bearer'}
)

incorrect_data = HTTPException(
    status_code=401,
    detail='Incorrect username or password',
    headers={'WWW-Authenticate': 'Bearer'}
)


not_unique = HTTPException(
    status_code=403,
    detail='User with this username already exists'
)
