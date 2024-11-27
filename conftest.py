from app.config import settings
import pytest
from app.database import engine, Base


def pytest_configure():
    settings.ENVIRONMENT = "TEST"


@pytest.fixture(scope="function", autouse=True)
def setup_and_teardown():
    Base.metadata.create_all(bind=engine)
    yield
    Base.metadata.drop_all(bind=engine)
