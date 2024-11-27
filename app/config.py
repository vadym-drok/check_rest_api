from pydantic import EmailStr
from pydantic_settings import BaseSettings


class Settings(BaseSettings):
    DB_USER_NAME: str
    DB_USER_PASSWORD: str
    DB_NAME: str
    DB_HOST: str
    DB_PORT: int
    DB_DRIVER: str
    PGADMIN_EMAIL: EmailStr
    PGADMIN_PASSWORD: str
    SECRET_KEY: str
    ALGORITHM: str
    ACCESS_TOKEN_EXPIRE_MINUTES: int
    ENVIRONMENT: str

    class Config:
        env_file = '.env'

    def add_db_driver(self):
        return f'+{self.DB_DRIVER}'


settings = Settings()
