from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from core import config, register_exception_handler

# import api_router
from modules import api_router


app = FastAPI()

app.include_router(api_router)

# CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=[config.VITE_API_URL],
    allow_credentials=True,
    allow_methods=['GET', 'POST', 'PUT', 'PATCH', 'DELETE'],
    allow_headers=['*']
)

# exception handlers
register_exception_handler(app)
