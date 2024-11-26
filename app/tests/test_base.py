from fastapi.testclient import TestClient
from app.main import app
from fastapi import status


client = TestClient(app)


def test_root():
    response = client.get("/")
    assert response.status_code == status.HTTP_200_OK


def test_register_user():
    post_data = {
        "first_name": "test_first_name",
        "last_name": "Test_last_name",
        "username": "test_username_6",
        "password": "test_password"
    }
    response = client.post("/users", json=post_data)
    response_data = response.json()

    assert response.status_code == status.HTTP_201_CREATED
    assert response_data.pop("created_at")
    assert response_data == {
        "first_name": "test_first_name",
        "last_name": "Test_last_name",
        "username": "test_username_6",
    }
