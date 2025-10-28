from re import match
from pydantic import BaseModel, Field, field_validator
from uuid import UUID


class TokenResponse(BaseModel):

    access_token: str
    token_type: str = 'bearer'


class UserResponse(BaseModel):
    model_config = {
        'from_attributes': True
    }

    id: UUID
    username: str
    full_name: str | None = None


class UserPost(BaseModel):
    model_config = {
        'extra': 'forbid'
    }

    username: str = Field(max_length=50)
    password: str = Field(max_length=50)

    @field_validator('username')
    def verify_username(cls, value):
        pattern = r'^(?=[A-Za-z])(?=.*[A-Z])(?=.*[a-z])(?=.*\d)[A-Za-z\d_]{1,50}$'
        if not match(pattern, value):
            raise ValueError('Foydalanuvchi nomi yaroqsiz')
        return value

    @field_validator('password')
    def verify_password(cls, value):
        pattern = r'^(?=[A-Za-z])(?=.*[A-Z])(?=.*[a-z])(?=.*\d)[A-Za-z\d_]{8,50}$'
        if not match(pattern, value):
            raise ValueError('Parol juda zaif. Kuchliroq parol kiriting.')
        return value


class UserUpdate(BaseModel):
    model_config = {
        'extra': 'forbid'
    }

    username: str | None = Field(None, max_length=50)
    password: str | None = Field(None, max_length=50)
    full_name: str | None = Field(None, max_length=50, pattern=r'^[A-Za-z -]{1,50}')

    @field_validator('username')
    def verify_username(cls, value):
        pattern = r'^(?=[A-Za-z])(?=.*[A-Z])(?=.*[a-z])(?=.*\d)[A-Za-z\d_]{1,50}$'
        if not match(pattern, value):
            raise ValueError('Foydalanuvchi nomi yaroqsiz')
        return value

    @field_validator('password')
    def verify_password(cls, value):
        pattern = r'^(?=[A-Za-z])(?=.*[A-Z])(?=.*[a-z])(?=.*\d)[A-Za-z\d_]{8,50}$'
        if not match(pattern, value):
            raise ValueError('Parol juda zaif. Kuchliroq parol kiriting.')
        return value