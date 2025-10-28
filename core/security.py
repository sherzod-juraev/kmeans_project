from hashlib import sha256
from typing import Annotated
from datetime import datetime, timedelta
from passlib.context import CryptContext
from fastapi import Depends, HTTPException, status
from fastapi.security import OAuth2PasswordBearer
from jose import jwt, ExpiredSignatureError, JWTError
from uuid import UUID
from core import config


context = CryptContext(schemes=['bcrypt'], deprecated='auto')

oauth2_scheme = OAuth2PasswordBearer(tokenUrl='/auth/sign/up')
# password hash

def password_hashed(password: str, /) -> str:
    sha = sha256(password.encode('utf-8')).hexdigest()
    return context.hash(sha)

def verify_password(password: str, hash_password: str, /) -> bool:
    sha = sha256(password.encode('utf-8')).hexdigest()
    return context.verify(sha, hash_password)



def create_access_token(auth_id: UUID, /) -> str:
    token_dict = {
        'sub': str(auth_id),
        'exp': datetime.utcnow() + timedelta(minutes=config.ACCESS_TOKEN_MINUTES)
    }

    access_token = jwt.encode(token_dict, config.SECRET_KEY, algorithm=config.ALGORITHM)
    return access_token

def create_refresh_token(auth_id: UUID, /) -> str:
    token_dict = {
        'sub': str(auth_id),
        'exp': datetime.utcnow() + timedelta(days=config.REFRESH_TOKEN_DAYS)
    }
    refresh_token = jwt.encode(token_dict, config.SECRET_KEY, algorithm=config.ALGORITHM)
    return refresh_token


def verify_access_token(access_token: Annotated[str, Depends(oauth2_scheme)]) -> UUID:
    try:
        payload = jwt.decode(access_token, config.SECRET_KEY, algorithms=[config.ALGORITHM])
        auth_id = payload.get('sub')
        if not auth_id:
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail='Auth_id not found'
            )
        return UUID(auth_id)
    except ExpiredSignatureError:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail='Token expired',
            headers={
                'WWW-Authenticate': 'Bearer'
            }
        )
    except JWTError:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail='Token invalid',
            headers={
                'WWW-Authenticate': 'Bearer'
            }
        )


def verify_refresh_token(refresh_token: str, /) -> UUID:
    if not refresh_token:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail='Refresh token not found'
        )
    try:
        payload = jwt.decode(refresh_token, config.SECRET_KEY, algorithms=[config.ALGORITHM])
        auth_id = payload.get('sub')
        if not auth_id:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail='auth_id not found'
            )
        return UUID(auth_id)
    except ExpiredSignatureError:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail='Refresh token expired'
        )
    except JWTError:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail='Refresh token invalid'
        )