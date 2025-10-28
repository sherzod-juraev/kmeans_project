from typing import Annotated
from fastapi import APIRouter, Depends, Response, Request, status
from fastapi.security import OAuth2PasswordRequestForm
from database import get_db
from core import create_refresh_token, create_access_token, verify_access_token, verify_refresh_token, config
from . import User, UserPost, UserUpdate, UserResponse, TokenResponse, crud
from sqlalchemy.ext.asyncio import AsyncSession
from uuid import UUID

user_router = APIRouter()


@user_router.post(
    '/sign/up',
    summary='Create user',
    status_code=status.HTTP_201_CREATED,
    response_model=TokenResponse
)
async def create_user(
        response: Response,
        form_data: Annotated[OAuth2PasswordRequestForm, Depends()],
        db: Annotated[AsyncSession, Depends(get_db)]
) -> TokenResponse:
    user_scheme = UserPost(
        username=form_data.username,
        password=form_data.password
    )
    user_db = await crud.create_user(db, user_scheme)
    response.set_cookie(
        key='refresh_token',
        value=create_refresh_token(user_db.id),
        max_age=60 * 60 * 24 * config.REFRESH_TOKEN_DAYS,
        samesite='strict',
        httponly=True
    )
    token = TokenResponse(
        access_token=create_access_token(user_db.id)
    )
    return token


@user_router.post(
    '/refresh/token',
    summary='Update access token',
    status_code=status.HTTP_200_OK,
    response_model=TokenResponse
)
async def update_access_token(
        request: Request,
        response: Response,
        db: Annotated[AsyncSession, Depends(get_db)]
) -> TokenResponse:
    refresh_token = request.cookies.get('refresh_token')
    auth_id = verify_refresh_token(refresh_token)
    response.set_cookie(
        key='refresh_token',
        value=create_refresh_token(auth_id),
        max_age=60 * 60 * 24 * config.REFRESH_TOKEN_DAYS,
        samesite='strict',
        httponly=True
    )
    token = TokenResponse(
        access_token=create_access_token(auth_id)
    )
    return token


@user_router.put(
    '/',
    summary='Full update user',
    status_code=status.HTTP_200_OK,
    response_model=UserResponse
)
async def full_update(
        auth_id: Annotated[UUID, Depends(verify_access_token)],
        user_scheme: UserUpdate,
        db: Annotated[AsyncSession, Depends(get_db)]
) -> User:
    user_db = await crud.update_user(db, user_scheme, auth_id)
    return user_db


@user_router.patch(
    '/',
    summary='Partial update user',
    status_code=status.HTTP_200_OK,
    response_model=UserResponse
)
async def partial_update(
        auth_id: Annotated[UUID, Depends(verify_access_token)],
        user_scheme: UserUpdate,
        db: Annotated[AsyncSession, Depends(get_db)]
) -> User:
    user_db = await crud.update_user(db, user_scheme, auth_id, True)
    return user_db


@user_router.delete(
    '/',
    summary='Delete user',
    status_code=status.HTTP_204_NO_CONTENT,
    response_model=None
)
async def delete_user(
        response: Response,
        auth_id: Annotated[UUID, Depends(verify_access_token)],
        user_scheme: UserPost,
        db: Annotated[AsyncSession, Depends(get_db)]
) -> None:
    await crud.delete_user(db, user_scheme, auth_id)
    response.delete_cookie('refresh_token')


@user_router.get(
    '/',
    summary='Get user',
    status_code=status.HTTP_200_OK,
    response_model=UserResponse
)
async def get_user(
        auth_id: Annotated[UUID, Depends(verify_access_token)],
        db: Annotated[AsyncSession, Depends(get_db)]
) -> User:
    user_db = await crud.verify_user_by_id(db, auth_id)
    return user_db