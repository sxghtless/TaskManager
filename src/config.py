import os

from pydantic import Extra
from pydantic_settings import BaseSettings


class Settings(BaseSettings, extra=Extra.ignore):
    host: str = '0.0.0.0'
    port: int = 8000
    app_name: str = 'taskmanager'
    project_path: str = os.path.dirname(__file__)
    POSTGRES_HOST: str = ''
    POSTGRES_USER: str = ''
    POSTGRES_PASSWORD: str = ''
    POSTGRES_PORT: str = ''
    POSTGRES_DB: str = ''
    REDIS_URL: str = ''


    @property
    def database_url(self):
        return f'postgresql://{self.POSTGRES_USER}:{self.POSTGRES_PASSWORD}@{self.POSTGRES_HOST}:{self.POSTGRES_PORT}/{self.POSTGRES_DB}'


def get_settings():
    return Settings()
