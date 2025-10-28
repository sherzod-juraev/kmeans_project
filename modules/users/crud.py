from . import User, UserUpdate, UserPost
from core import password_hashed, verify_password
from sqlalchemy import delete
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.exc import IntegrityError
from fastapi import HTTPException, status
from uuid import UUID


async def save_to_db(
        db: AsyncSession,
        user_db: User,
        /
) -> User:
    try:
        await db.commit()
        await db.refresh(user_db)
        return user_db
    except IntegrityError as exc:
        await db.rollback()
        error_msg = str(exc.orig)
        if 'ix_users_username' in error_msg:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail='Username already exists'
            )
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail='Error creating user'
        )


async def create_user(
        db: AsyncSession,
        user_scheme: UserPost,
        /
) -> User:
    user_db = User(
        username=user_scheme.username,
        password=password_hashed(user_scheme.password)
    )
    db.add(user_db)
    user_db = await save_to_db(db, user_db)
    return user_db


async def update_user(
        db: AsyncSession,
        user_scheme: UserUpdate,
        auth_id: UUID,
        exclude_unset: bool = False,
        /
) -> User:
    user_db = await verify_user_by_id(db, auth_id)
    for field, value in user_scheme.model_dump(exclude_unset=exclude_unset).items():
        if field == 'password':
            setattr(user_db, field, password_hashed(value))
        else:
            setattr(user_db, field, value)
    user_db = await save_to_db(db, user_db)
    return user_db


async def delete_user(
        db: AsyncSession,
        user_scheme: UserPost,
        auth_id,
        /
) -> None:
    user_db = await verify_user_by_id(db, auth_id)
    await verify_fields(user_db, user_scheme)
    query = delete(User).where(User.username==user_scheme.username)
    result = await db.execute(query)
    await db.commit()
    if result.rowcount == 0:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail='User not found'
        )


async def verify_fields(user_db: User, user_scheme: UserPost, /) -> None:
    username = user_scheme.username != user_db.username
    password = verify_password(user_scheme.password, user_db.password)
    if username and not password:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail='Username and password is wrong'
        )
    elif username:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail='Username is wrong'
        )
    elif not password:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail='Password is wrong'
        )


async def verify_user_by_id(
        db: AsyncSession,
        auth_id: UUID,
        /
) -> User:
    user_db = await db.get(User, auth_id)
    if not user_db:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail='User not found'
        )
    return user_db