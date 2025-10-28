from pydantic import BaseModel


class Tag(BaseModel):

    users: str = 'Authenticate'
    chats: str = 'Chats'
    centers: str = 'Centers'
    learns: str = 'Learn data'

tags = Tag()