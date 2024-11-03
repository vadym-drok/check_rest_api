from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
from app.config import settings


SQLALCHEMY_DATABASE_URL = f'postgresql{settings.add_db_driver()}://' \
                          f'{settings.db_user_name}:{settings.db_user_password}' \
                          f'@{settings.db_host}:{settings.db_port}/{settings.db_name}'

engine = create_engine(SQLALCHEMY_DATABASE_URL)

SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

Base = declarative_base()


def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()
