import pytest
from fastapi.testclient import TestClient

from app.main import app
from app.config import settings
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from app.database import get_db, Base

import psycopg2
from psycopg2.extensions import ISOLATION_LEVEL_AUTOCOMMIT


TEST_DB_NAME = 'test_db'


def connect_to_test_db():
    conn = psycopg2.connect(
        user=settings.DB_USER_NAME, password=settings.DB_USER_PASSWORD, host=settings.DB_HOST, port=settings.DB_PORT
    )
    conn.set_isolation_level(ISOLATION_LEVEL_AUTOCOMMIT)

    return conn


def create_test_database():
    conn = connect_to_test_db()
    cur = conn.cursor()

    cur.execute(f"CREATE DATABASE {TEST_DB_NAME};")
    cur.close()
    conn.close()


def drop_test_database():
    conn = connect_to_test_db()
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


# @pytest.fixture(scope="function", autouse=True)
# def setup_and_teardown():
    # Base.metadata.create_all(bind=engine)
    # yield
    # Base.metadata.drop_all(bind=engine)


@pytest.fixture()
def api_client():
    SQLALCHEMY_DATABASE_URL = f'postgresql{settings.add_db_driver()}://' \
                              f'{settings.DB_USER_NAME}:{settings.DB_USER_PASSWORD}' \
                              f'@{settings.DB_HOST}:{settings.DB_PORT}/test_db'

    engine = create_engine(SQLALCHEMY_DATABASE_URL)
    TestingSessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

    Base.metadata.create_all(bind=engine)

    def override_get_db():
        db = TestingSessionLocal()
        try:
            yield db
        finally:
            db.close()

    client = TestClient(app)

    app.dependency_overrides[get_db] = override_get_db

    yield client

    Base.metadata.drop_all(bind=engine)
