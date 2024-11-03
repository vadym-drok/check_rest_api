from pydantic import EmailStr
from pydantic_settings import BaseSettings


class Settings(BaseSettings):
    db_user_name: str
    db_user_password: str
    db_name: str
    db_host: str
    db_port: int
    db_driver: str
    secret_key: str
    algorithm: str
    access_token_expire_minutes: int
    pgadmin_email: EmailStr
    pgadmin_password: str

    class Config:
        env_file = '.env'

    def add_db_driver(self):
        return f'+{self.db_driver}'


settings = Settings()
