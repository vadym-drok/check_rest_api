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

from app.models import User, Receipt
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
def registered_user(db_session):
    user_data = {
        "first_name": "test_first_name",
        "last_name": "Test_last_name",
        "username": "test_username_1",
        "password": get_password_hash("test_password")
    }

    new_user = User(**user_data)
    db_session.add(new_user)
    db_session.commit()
    db_session.refresh(new_user)

    return new_user


@pytest.fixture()
def second_user(db_session):
    user_data = {
        "first_name": "test_second_name",
        "last_name": "Test_last_name",
        "username": "test_username_2",
        "password": get_password_hash("test_password")
    }

    new_user = User(**user_data)
    db_session.add(new_user)
    db_session.commit()
    db_session.refresh(new_user)

    return new_user


@pytest.fixture()
def authorized_client(api_client, registered_user):
    token_data = {"username": registered_user.username}
    access_token = create_access_token(token_data)

    api_client.headers.update({
        "Authorization": f"Bearer {access_token.access_token}"
    })

    return api_client, registered_user


@pytest.fixture()
def create_receipt(registered_user, db_session):
    def factory(receipt_data, current_user=registered_user):
        receipt_create = ReceiptCreate(**receipt_data)
        receipt = create_receipt_record(db=db_session, current_user=current_user, receipt_data=receipt_create)
        return receipt

    return factory


@pytest.fixture()
def receipt(create_receipt):
    receipt_data = {
        "products": [
            {
                "name": "product_1",
                "price": 1,
                "quantity": 2,
                "add_field_1": "test_1",
                "add_field_2": "test_2"
            },
            {
                "name": "product_2",
                "price": 0.2,
                "quantity": 20,
                "add_field_3": "test_3"
            }
        ],
        "payment": {
            "type": "cash",
            "amount": 100
        }
    }
    receipt = create_receipt(receipt_data)
    return receipt


@pytest.fixture()
def receipts(create_receipt, db_session):
    receipts_data = [
        {
            "products": [{"name": "product_1", "price": 1, "quantity": 2}],
            "payment": {
                "type": "cash",
                "amount": 100
            }
        },
        {
            "products": [{"name": "product_2", "price": 1, "quantity": 10}],
            "payment": {
                "type": "cashless",
                "amount": 100
            }
        },
        {
            "products": [{"name": "product_3", "price": 1, "quantity": 5}],
            "payment": {
                "type": "cashless",
                "amount": 100
            }
        },
        {
            "products": [{"name": "product_4", "price": 1, "quantity": 15}],
            "payment": {
                "type": "cash",
                "amount": 100
            }
        },
        {
            "products": [{"name": "product_5", "price": 1, "quantity": 2}],
            "payment": {
                "type": "cash",
                "amount": 100
            }
        },
        {
            "products": [{"name": "product_6", "price": 1, "quantity": 13}],
            "payment": {
                "type": "cash",
                "amount": 100
            }
        },
    ]
    receipt_ids = []
    for receipt_data in receipts_data:
        receipt = create_receipt(receipt_data)
        receipt_ids.append(receipt.id)

    receipts = db_session.query(Receipt).filter(Receipt.id.in_(receipt_ids))
    return receipts


@pytest.fixture()
def second_user_receipt(create_receipt, second_user):
    receipt_data = {
        "products": [
            {
                "name": "product_second_user",
                "price": 1,
                "quantity": 3,
            },
        ],
        "payment": {
            "type": "cash",
            "amount": 10
        }
    }
    receipt = create_receipt(receipt_data, current_user=second_user)
    return receipt
