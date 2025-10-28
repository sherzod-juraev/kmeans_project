from typing import Annotated
from fastapi import APIRouter, Depends, status
from sqlalchemy.ext.asyncio import AsyncSession
from database import get_db
from core import verify_access_token
from uuid import UUID
from . import Chat, ChatPost, ChatResponse, crud
from modules.centers.crud import verify_centers


chat_router = APIRouter()


@chat_router.post(
    '/',
    summary='Create chat',
    status_code=status.HTTP_201_CREATED,
    response_model=ChatResponse
)
async def create_chat(
        auth_id: Annotated[UUID, Depends(verify_access_token)],
        chat_scheme: ChatPost,
        db: Annotated[AsyncSession, Depends(get_db)]
) -> Chat:
    chat_db = await crud.create_chat(db, chat_scheme, auth_id)
    return chat_db


@chat_router.delete(
    '/{chat_id}',
    summary='Delete chat',
    status_code=status.HTTP_204_NO_CONTENT,
    response_model=None,
    dependencies=[Depends(verify_access_token)]
)
async def delete_chat(
        chat_id: UUID,
        db: Annotated[AsyncSession, Depends(get_db)]
) -> None:
    await crud.delete_chat(db, chat_id)


@chat_router.get(
    '/all',
    summary='Get all chats',
    status_code=status.HTTP_200_OK,
    response_model=list[ChatResponse]
)
async def get_all_chats(
        auth_id: Annotated[UUID, Depends(verify_access_token)],
        db: Annotated[AsyncSession, Depends(get_db)],
        skip: int = 0,
        limit: int = 10
) -> list[Chat]:
    chats = await crud.get_all_chats_by_user_id(db, auth_id, skip, limit)
    return chats


@chat_router.get(
    '/{chat_id}',
    summary='Get chat',
    status_code=status.HTTP_200_OK,
    response_model=dict,
    dependencies=[Depends(verify_access_token)]
)
async def get_chat(
        chat_id: UUID,
        db: Annotated[AsyncSession, Depends(get_db)]
) -> dict:
    chat_db = await crud.verify_chat_by_id(db, chat_id)
    centers = await verify_centers(db, chat_id)
    chat_dict = {
        'id': chat_db.id,
        'title': chat_db.title,
        'coordinates': centers
    }
    return chat_dict