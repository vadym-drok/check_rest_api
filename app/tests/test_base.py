from fastapi import status


def test_root(api_client):
    response = api_client.get("/")
    assert response.status_code == status.HTTP_200_OK


def test_register_user(api_client):
    post_data = {
        "first_name": "test_first_name",
        "last_name": "Test_last_name",
        "username": "test_username_6",
        "password": "test_password"
    }
    response = api_client.post("/users", json=post_data)
    response_data = response.json()

    assert response.status_code == status.HTTP_201_CREATED
    assert response_data.pop("created_at")
    assert response_data == {
        "first_name": "test_first_name",
        "last_name": "Test_last_name",
        "username": "test_username_6",
    }


def test_register_user_duplicate(api_client, registered_client):
    response = api_client.post("/users", json={
        "first_name": registered_client.first_name,
        "last_name": registered_client.last_name,
        "username": registered_client.username,
        "password": "test_password"
    })
    response_data = response.json()

    assert response.status_code == status.HTTP_400_BAD_REQUEST
    assert response_data['detail'] == 'Username already registered'


def test_user_login(api_client, registered_client):
    post_data = {
        "username": registered_client.username,
        "password": "test_password",
        "grant_type": "password",
    }
    response = api_client.post("/login", data=post_data)
    response_data = response.json()

    assert response.status_code == status.HTTP_200_OK
    assert response_data["access_token"]
    assert response_data["token_type"] == "bearer"
