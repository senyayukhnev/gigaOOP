from contextlib import asynccontextmanager
import uuid

from fastapi import Depends, FastAPI
from fastapi_users import FastAPIUsers

from auth.db import User, create_db_and_tables
from auth.schemas import UserCreate, UserRead, UserUpdate
from auth.users import current_active_user, fastapi_users, get_user_manager
from auth.auth import auth_backend
from core.config import settings

from fastapi.middleware.cors import CORSMiddleware
import logging

# Настройка логирования
logging.basicConfig(level=logging.DEBUG)


@asynccontextmanager
async def lifespan(app: FastAPI):
    await create_db_and_tables()
    yield

fastapi_users = FastAPIUsers[User, uuid.UUID](
    get_user_manager,
    [auth_backend],
)

app = FastAPI(title=settings.PROJECT_NAME, version=settings.PROJECT_VERSION, lifespan=lifespan)

app.include_router(
    fastapi_users.get_auth_router(auth_backend),
    prefix="/auth/jwt",
    tags=["auth"]
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


origins = [
    'http://localhost',
    'http://localhost:5173',
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=['GET, POST, PATCH, DELETE'],
    allow_headers=['*'],
)


@app.get("/authenticated-route")
async def authenticated_route(user: User = Depends(current_active_user)):
    return {"message": f"Hello {user.email}!"}
