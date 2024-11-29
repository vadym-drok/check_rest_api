from fastapi import status
import pytest


def test_root(api_client):
    response = api_client.get("/")
    assert response.status_code == status.HTTP_200_OK


def test_register_user(api_client):
    post_data = {
        "first_name": "test_first_name",
        "last_name": "Test_last_name",
        "username": "test_username_1",
        "password": "test_password"
    }
    response = api_client.post("/users", json=post_data)
    response_data = response.json()

    assert response.status_code == status.HTTP_201_CREATED
    assert response_data.pop("created_at")
    assert response_data == {
        "first_name": "test_first_name",
        "last_name": "Test_last_name",
        "username": "test_username_1",
    }


def test_register_user_duplicate(api_client, registered_user):
    response = api_client.post("/users", json={
        "first_name": registered_user.first_name,
        "last_name": registered_user.last_name,
        "username": registered_user.username,
        "password": "test_password"
    })
    response_data = response.json()

    assert response.status_code == status.HTTP_400_BAD_REQUEST
    assert response_data['detail'] == 'Username already registered'


def test_user_login(api_client, registered_user):
    post_data = {
        "username": registered_user.username,
        "password": "test_password",
        "grant_type": "password",
    }
    response = api_client.post("/login", data=post_data)
    response_data = response.json()

    assert response.status_code == status.HTTP_200_OK
    assert response_data["access_token"]
    assert response_data["token_type"] == "bearer"


@pytest.mark.parametrize(
    "add_post_data, response_status_code",
    [
        ({}, status.HTTP_422_UNPROCESSABLE_ENTITY),
        ({"password": "test_password_1"}, status.HTTP_401_UNAUTHORIZED),
    ]
)
def test_user_login_failed(add_post_data, response_status_code, api_client, registered_user):
    post_data = {
        "username": registered_user.username,
        "grant_type": "password",
        **add_post_data,
    }
    response = api_client.post("/login", data=post_data)
    response_data = response.json()

    assert "access_token" not in response_data
    assert response.status_code ==  response_status_code
