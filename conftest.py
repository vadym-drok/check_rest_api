import pytest
from fastapi.testclient import TestClient

from app.crud import create_access_token, create_receipt_record
from app.main import app
from app.config import settings
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from app.database import get_db, Base

import psycopg2
from psycopg2.extensions import ISOLATION_LEVEL_AUTOCOMMIT

from app.models import User
from app.schemas import ReceiptCreate
from app.utils import get_password_hash


TEST_DB_NAME = 'test_db'


def connect_for_db():
    conn = psycopg2.connect(
        user=settings.DB_USER_NAME, password=settings.DB_USER_PASSWORD, host=settings.DB_HOST, port=settings.DB_PORT
    )
    conn.set_isolation_level(ISOLATION_LEVEL_AUTOCOMMIT)

    return conn


def create_test_database():
    conn = connect_for_db()
    cur = conn.cursor()

    cur.execute(f"CREATE DATABASE {TEST_DB_NAME};")
    cur.close()
    conn.close()


def drop_test_database():
    conn = connect_for_db()
    cur = conn.cursor()

    cur.execute(
        f"SELECT pg_terminate_backend(pg_stat_activity.pid) "
        f"FROM pg_stat_activity "
        f"WHERE pg_stat_activity.datname = '{TEST_DB_NAME}';"
    )
    cur.execute(f"DROP DATABASE IF EXISTS {TEST_DB_NAME};")
    cur.close()
    conn.close()


@pytest.fixture(scope="session", autouse=True)
def setup_test_db():
    create_test_database()
    yield
    drop_test_database()


@pytest.fixture(scope="function")
def db_session():
    SQLALCHEMY_DATABASE_URL = f'postgresql+psycopg2://' \
                              f'{settings.DB_USER_NAME}:{settings.DB_USER_PASSWORD}' \
                              f'@{settings.DB_HOST}:{settings.DB_PORT}/{TEST_DB_NAME}'

    engine = create_engine(SQLALCHEMY_DATABASE_URL)
    TestingSessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

    Base.metadata.create_all(bind=engine)

    db = TestingSessionLocal()

    yield db

    db.close()

    Base.metadata.drop_all(bind=engine)


@pytest.fixture()
def api_client(db_session):
    def override_get_db():
        try:
            yield db_session
        finally:
            db_session.close()

    app.dependency_overrides[get_db] = override_get_db
    client = TestClient(app)

    yield client

    app.dependency_overrides.clear()


@pytest.fixture()
def registered_client(db_session):
    user_data = {
        "first_name": "test_first_name",
        "last_name": "Test_last_name",
        "username": "test_username_6",
        "password": get_password_hash("test_password")
    }

    new_user = User(**user_data)
    db_session.add(new_user)
    db_session.commit()
    db_session.refresh(new_user)

    return new_user


@pytest.fixture()
def authorized_client(api_client, registered_client):
    token_data = {"username": registered_client.username}
    access_token = create_access_token(token_data)

    api_client.headers.update({
        "Authorization": f"Bearer {access_token.access_token}"
    })

    return api_client, registered_client


@pytest.fixture()
def create_receipt(registered_client, db_session):
    def factory(receipt_data):
        receipt_create = ReceiptCreate(**receipt_data)
        receipt = create_receipt_record(db=db_session, current_user=registered_client, receipt_data=receipt_create)
        return receipt

    return factory
