from dotenv import load_dotenv
from os import getenv
from pydantic import BaseModel


# opening .env
load_dotenv()

class Config(BaseModel):

    DATABASE_URL: str = getenv('DATABASE_URL')
    ACCESS_TOKEN_MINUTES: int = int(getenv('ACCESS_TOKEN_MINUTES'))
    REFRESH_TOKEN_DAYS: int = int(getenv('REFRESH_TOKEN_DAYS'))
    SECRET_KEY: str = getenv('SECRET_KEY')
    ALGORITHM: str = getenv('ALGORITHM')
    VITE_API_URL: str = getenv('VITE_API_URL')

config = Config()