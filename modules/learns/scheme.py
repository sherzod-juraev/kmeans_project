from pydantic import BaseModel
from uuid import UUID

class DataPost(BaseModel):
    model_config = {
        'extra': 'forbid'
    }

    array: list[float]
    chat_id: UUID