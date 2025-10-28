from typing import Annotated
from fastapi import APIRouter, Depends, status
from sqlalchemy.ext.asyncio import AsyncSession
from uuid import UUID
from database import get_db
from . import Center, CenterPost, CenterResponse, crud


center_router = APIRouter()


@center_router.post(
    '/',
    summary='Create centers',
    status_code=status.HTTP_201_CREATED,
    response_model=CenterResponse
)
async def create_centers(
        center_scheme: list[CenterPost],
        db: Annotated[AsyncSession, Depends(get_db)]
) -> CenterResponse:
    center_db = await crud.create_centers(db, center_scheme)
    center_scheme = CenterResponse(
        id=center_db.id,
        value=list(center_db.value)
    )
    return center_scheme


@center_router.get(
    '/{chat_id}',
    summary='Get centers by chat_id',
    status_code=status.HTTP_200_OK,
    response_model=list[CenterResponse]
)
async def get_centers(
        chat_id: UUID,
        db: Annotated[AsyncSession, Depends(get_db)]
) -> list[Center]:
    centers_db = await crud.verify_centers(db, chat_id)
    return centers_db