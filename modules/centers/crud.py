from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.exc import IntegrityError
from sqlalchemy import select
from . import Center, CenterPost
from fastapi import HTTPException, status
from uuid import UUID
from kmeans_model import kmeans
from numpy import array


async def save_to_db(
        db: AsyncSession,
        center_db: Center,
        /
) -> Center:
    try:
        await db.commit()
        await db.refresh(center_db)
        return center_db
    except IntegrityError as exc:
        await db.rollback()
        error_msg = str(exc.orig)
        if 'centers_chat_id_fkey' in error_msg:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail='Chat not found'
            )
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail='Error creating center'
        )


async def create_centers(
        db: AsyncSession,
        center_scheme: list[CenterPost],
        /
) -> Center:
    length = len(center_scheme)
    array = []
    for i in range(length):
        array.append(center_scheme[i].coordinates)
    center_db = Center(
        value=array,
        k=kmeans.k,
        chat_id=center_scheme[0].chat_id
    )
    db.add(center_db)
    center_db = await save_to_db(db, center_db)
    return center_db


async def verify_centers(
        db: AsyncSession,
        chat_id: UUID,
        /
) -> list[Center]:
    query = select(Center).where(Center.chat_id == chat_id).order_by(Center.created_at.desc())
    result = await db.execute(query)
    centers = result.scalars().first()
    if not centers:
        return centers
    # kmeans modelini moslashtirish
    kmeans.centers = array(centers.value)
    kmeans.k = centers.k
    kmeans.set_property(len(centers.value[0]))
    return centers.value