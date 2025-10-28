from pydantic import BaseModel
from uuid import UUID


class CenterResponse(BaseModel):
    model_config = {
        'from_attributes': True
    }

    id: UUID
    value: list[list[float]]


class CenterPost(BaseModel):
    model_config = {
        'extra': 'forbid'
    }

    coordinates: list[float]
    chat_id: UUID