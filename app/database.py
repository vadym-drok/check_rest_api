from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, declarative_base
from app.config import settings


SQLALCHEMY_DATABASE_URL = f'postgresql{settings.add_db_driver()}://' \
                          f'{settings.DB_USER_NAME}:{settings.DB_USER_PASSWORD}' \
                          f'@{settings.DB_HOST}:{settings.DB_PORT}/{settings.DB_NAME}'

engine = create_engine(SQLALCHEMY_DATABASE_URL)

SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

Base = declarative_base()


def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()
