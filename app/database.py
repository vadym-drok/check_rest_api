from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
from app.config import settings


db_name = 'test_db' if settings.ENVIRONMENT == 'TEST' else settings.DB_NAME

SQLALCHEMY_DATABASE_URL = f'postgresql{settings.add_db_driver()}://' \
                          f'{settings.DB_USER_NAME}:{settings.DB_USER_PASSWORD}' \
                          f'@{settings.DB_HOST}:{settings.DB_PORT}/{db_name}'

engine = create_engine(SQLALCHEMY_DATABASE_URL)

SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

Base = declarative_base()


def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()
