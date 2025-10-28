from pydantic import BaseModel

class Prefix(BaseModel):

    users: str = '/auth'
    chats: str = '/chats'
    centers: str = '/centers'
    learns: str = '/learn'


prefixes = Prefix()