import pytest
from jose import JWTError, jwt
from app import schemas
from app.config import settings


def test_root(client):
    res = client.get("/")
    print(res.json().get('message'))
    assert res.json().get('message') == "Hello World DOCKER"
    assert res.status_code == 200


def test_create_user(client):
    res = client.post(
        "/users", json={"email": "hello123@gmail.com", "password": "password123"})
    new_user = schemas.UserOut(**res.json()) #validate the output against the model
    assert new_user.email == "hello123@gmail.com"
    assert res.status_code == 201


def test_login_user(client, test_user):
    res = client.post(
        "/login", data={"username": test_user['email'], "password": test_user['password']})
    login_res = schemas.Token(**res.json())

    payload=jwt.decode(login_res.access_token, settings.secret_key, settings.algorithm)
    id: str = payload.get("user_id")

    assert id == test_user['user_id']
    assert login_res.token_type == "bearer"
    assert res.status_code == 201


@pytest.mark.parametrize("email, password, status_code", [
    ('wrongemail@gmail.com', 'password123', 403),
    ('hello123@gmail.com', 'wrongpassword', 403),
    ('wrongemail@gmail.com', 'wrongpassword', 403),
    (None, 'password123', 422),
    ('jb123@gmail.com', None, 422)
])
def test_incorrect_login(test_user, client, email, password, status_code):
    res = client.post(
        "/login", data={"username": test_user['email'], "password": "wrongPASS"})

    assert res.status_code == 403
    assert res.json().get('detail') == "Invalid Credentials"

