from contextlib import asynccontextmanager
import uvicorn
from fastapi import FastAPI
from starlette.middleware.cors import CORSMiddleware
from src.auth.config import fastapi_users, auth_backend
from src.auth.schemas import UserRead, UserCreate, UserUpdate
from src.tasks.connection import Settings
from src.products import products_router
from src.orders import orders_router
from src.tasks import event_router

@asynccontextmanager
async def lifespan(app: FastAPI):
    settings = Settings()
    await settings.initialize_database()
    yield

app = FastAPI(lifespan=lifespan)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(
    fastapi_users.get_auth_router(auth_backend), prefix="/auth/jwt", tags=["auth"]
)
app.include_router(
    fastapi_users.get_register_router(UserRead, UserCreate),
    prefix="/auth",
    tags=["auth"],
)
app.include_router(
    fastapi_users.get_reset_password_router(),
    prefix="/auth",
    tags=["auth"],
)
app.include_router(
    fastapi_users.get_verify_router(UserRead),
    prefix="/auth",
    tags=["auth"],
)
app.include_router(
    fastapi_users.get_users_router(UserRead, UserUpdate),
    prefix="/users",
    tags=["users"],
)
app.include_router(
    products_router
)
app.include_router(
    orders_router
)
app.include_router(
    event_router
)


if __name__ == '__main__':
    uvicorn.run('main:app', reload=True)