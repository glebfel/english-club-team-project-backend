import pathlib
from dotenv import load_dotenv
from pydantic import BaseSettings, Field

# root directory
ROOT_PATH = str(pathlib.Path(__file__).parent.parent.parent)


class Settings(BaseSettings):
    # for main db
    POSTGRES_USER: str = Field(default='postgres', env='POSTGRES_USER')
    POSTGRES_PASSWORD: str = Field(..., env='POSTGRES_PASSWORD')
    POSTGRES_HOST: str = Field(default='localhost', env='POSTGRES_HOST')
    POSTGRES_PORT: int = Field(default=5433, env='POSTGRES_PORT')
    POSTGRES_DB: str = Field(default='postgres', env='POSTGRES_DB')
    # for api
    API_HOST: str = Field(default='localhost', env='API_HOST')
    API_PORT: int = Field(default=8080, env='API_PORT')
    API_VERSION: str = Field(default='1.0.0', env='API_VERSION')
    API_DESCRIPTION: str = Field(default='API service for child camp 🏕', env='API_DESCRIPTION')
    # api auth settings
    AUTH_SECRET_KEY: str = Field(..., env="AUTH_SECRET_KEY")
    ALGORITHM: str = Field(default='HS256', env="ALGORITHM")
    ACCESS_TOKEN_EXPIRE_MINUTES: int = Field(default=30, env="ACCESS_TOKEN_EXPIRE_MINUTES")

    class Config:
        env_prefix = ""
        case_sentive = False
        env_file = '.env'
        env_file_encoding = 'utf-8'


# load env from file
load_dotenv()

# load vars to settings
settings = Settings()