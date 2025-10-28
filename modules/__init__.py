from fastapi import APIRouter, Depends
from core import tags, prefixes, verify_access_token

# import models
from .users import User
from .chats.model import Chat
from .centers.model import Center

__all__ = ['User', 'Chat', 'Center']

# import routers
from .users.router import user_router
from .chats.router import chat_router
from .centers.router import center_router
from .learns.router import learn_router

api_router = APIRouter()

api_router.include_router(
    user_router,
    prefix=prefixes.users,
    tags=[tags.users]
)

api_router.include_router(
    chat_router,
    prefix=prefixes.chats,
    tags=[tags.chats]
)

api_router.include_router(
    center_router,
    prefix=prefixes.centers,
    tags=[tags.centers],
    dependencies=[Depends(verify_access_token)]
)

api_router.include_router(
    learn_router,
    prefix=prefixes.learns,
    tags=[tags.learns],
    dependencies=[Depends(verify_access_token)]
)