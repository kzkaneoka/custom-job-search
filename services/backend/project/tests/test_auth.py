import json

from flask import current_app

from project.tests.utils import add_user


def test_user_registration(test_app, test_database):
    client = test_app.test_client()
    resp = client.post(
        "/auth/register",
        data=json.dumps(
            {
                "username": "test_user_registration",
                "email": "test_user_registration@test.com",
                "password": "test_password",
            }
        ),
        content_type="application/json",
    )
    data = json.loads(resp.data.decode())
    assert resp.status_code == 201
    assert "Successfully registered." in data["message"]
    assert "success" in data["status"]
    assert data["auth_token"]
    assert resp.content_type == "application/json"


def test_user_registration_duplicate_email(test_app):
    add_user(
        "test_user_registration_duplicate_email1",
        "test_user_registration_duplicate_email@test.com",
        "test_password",
    )
    client = test_app.test_client()
    resp = client.post(
        "/auth/register",
        data=json.dumps(
            {
                "username": "test_user_registration_duplicate_email2",
                "email": "test_user_registration_duplicate_email@test.com",
                "password": "test_password",
            }
        ),
        content_type="application/json",
    )
    data = json.loads(resp.data.decode())
    assert resp.status_code == 400
    assert "Sorry. That user already exists." in data["message"]
    assert "fail" in data["status"]
    assert resp.content_type == "application/json"


def test_user_registration_duplicate_username(test_app):
    add_user(
        "test_user_registration_duplicate_username",
        "test_user_registration_duplicate_username1@test.com",
        "test_password",
    )
    client = test_app.test_client()
    resp = client.post(
        "/auth/register",
        data=json.dumps(
            {
                "username": "test_user_registration_duplicate_username",
                "email": "test_user_registration_duplicate_username2@test.com",
                "password": "test_password",
            }
        ),
        content_type="application/json",
    )
    data = json.loads(resp.data.decode())
    assert resp.status_code == 400
    assert "Sorry. That user already exists." in data["message"]
    assert "fail" in data["status"]
    assert resp.content_type == "application/json"


def test_user_registration_invalid_json(test_app):
    client = test_app.test_client()
    resp = client.post(
        "/auth/register", data=json.dumps({}), content_type="application/json",
    )
    data = json.loads(resp.data.decode())
    assert resp.status_code == 400
    assert "Invalid payload." in data["message"]
    assert "fail" in data["status"]
    assert resp.content_type == "application/json"


def test_user_registration_invalid_json_keys_no_username(test_app):
    client = test_app.test_client()
    resp = client.post(
        "/auth/register",
        data=json.dumps(
            {
                "email": "test_user_registration_invalid_json_keys_no_username@test.com",
                "password": "test_password",
            }
        ),
        content_type="application/json",
    )
    data = json.loads(resp.data.decode())
    assert resp.status_code == 400
    assert "Invalid payload." in data["message"]
    assert "fail" in data["status"]
    assert resp.content_type == "application/json"


def test_user_registration_invalid_json_keys_no_email(test_app):
    client = test_app.test_client()
    resp = client.post(
        "/auth/register",
        data=json.dumps(
            {
                "username": "test_user_registration_invalid_json_keys_no_email",
                "password": "test_password",
            }
        ),
        content_type="application/json",
    )
    data = json.loads(resp.data.decode())
    assert resp.status_code == 400
    assert "Invalid payload." in data["message"]
    assert "fail" in data["status"]
    assert resp.content_type == "application/json"


def test_user_registration_invalid_json_keys_no_password(test_app, test_database):
    client = test_app.test_client()
    resp = client.post(
        "/auth/register",
        data=json.dumps(
            {
                "username": "test_user_registration_invalid_json_keys_no_password",
                "email": "test_user_registration_invalid_json_keys_no_password@test.com",
            }
        ),
        content_type="application/json",
    )
    data = json.loads(resp.data.decode())
    assert resp.status_code == 400
    assert "Invalid payload." in data["message"]
    assert "fail" in data["status"]
    assert resp.content_type == "application/json"


def test_registered_user_login(test_app):
    add_user(
        "test_registered_user_login",
        "test_registered_user_login@test.com",
        "test_password",
    )
    client = test_app.test_client()
    resp = client.post(
        "/auth/login",
        data=json.dumps(
            {
                "email": "test_registered_user_login@test.com",
                "password": "test_password",
            }
        ),
        content_type="application/json",
    )
    data = json.loads(resp.data.decode())
    assert resp.status_code == 200
    assert "Successfully logged in." in data["message"]
    assert "success" in data["status"]
    assert data["auth_token"]
    assert resp.content_type == "application/json"


def test_not_registered_user_login(test_app, test_database):
    client = test_app.test_client()
    resp = client.post(
        "/auth/login",
        data=json.dumps(
            {
                "email": "test_not_registered_user_login@test.com",
                "password": "test_password",
            }
        ),
        content_type="application/json",
    )
    data = json.loads(resp.data.decode())
    assert resp.status_code == 404
    assert "User does not exist." in data["message"]
    assert "fail" in data["status"]
    assert resp.content_type == "application/json"


def test_valid_logout(test_app):
    add_user("test_valid_logout", "test_valid_logout@test.com", "test_password")
    client = test_app.test_client()
    # user login
    resp_login = client.post(
        "/auth/login",
        data=json.dumps(
            {"email": "test_valid_logout@test.com", "password": "test_password"}
        ),
        content_type="application/json",
    )
    # valid token logout
    token = json.loads(resp_login.data.decode())["auth_token"]
    resp = client.get(
        "/auth/logout",
        headers={"Authorization": f"Bearer {token}"},
        content_type="application/json",
    )
    data = json.loads(resp.data.decode())
    assert resp.status_code == 200
    assert "Successfully logged out." in data["message"]
    assert "success" in data["status"]
    assert resp.content_type == "application/json"


def test_invalid_logout_expired_token(test_app, test_database):
    add_user(
        "test_invalid_logout_expired_token",
        "test_invalid_logout_expired_token@test.com",
        "test_password",
    )
    current_app.config["TOKEN_EXPIRATION_SECONDS"] = -1
    client = test_app.test_client()
    # user login
    resp_login = client.post(
        "/auth/login",
        data=json.dumps(
            {
                "email": "test_invalid_logout_expired_token@test.com",
                "password": "test_password",
            }
        ),
        content_type="application/json",
    )
    # invalid token logout
    token = json.loads(resp_login.data.decode())["auth_token"]
    resp = client.get(
        "/auth/logout",
        headers={"Authorization": f"Bearer {token}"},
        content_type="application/json",
    )
    data = json.loads(resp.data.decode())
    assert resp.status_code == 401
    assert "Signature expired. Please log in again." in data["message"]
    assert "fail" in data["status"]
    assert resp.content_type == "application/json"
    current_app.config["TOKEN_EXPIRATION_SECONDS"] = 3


def test_user_status(test_app):
    add_user("test_user_status", "test_user_status@test.com", "test_password")
    client = test_app.test_client()
    resp_login = client.post(
        "/auth/login",
        data=json.dumps(
            {"email": "test_user_status@test.com", "password": "test_password"}
        ),
        content_type="application/json",
    )
    token = json.loads(resp_login.data.decode())["auth_token"]
    resp = client.get(
        "/auth/status",
        headers={"Authorization": f"Bearer {token}"},
        content_type="application/json",
    )
    data = json.loads(resp.data.decode())
    assert resp.status_code == 200
    assert "success" in data["status"]
    assert data["data"] is not None
    assert data["data"]["username"] == "test_user_status"
    assert data["data"]["email"] == "test_user_status@test.com"
    assert data["data"]["active"] is True
    assert resp.content_type == "application/json"


def test_invalid_status(test_app, test_database):
    client = test_app.test_client()
    resp = client.get(
        "/auth/status",
        headers={"Authorization": "Bearer invalid"},
        content_type="application/json",
    )
    data = json.loads(resp.data.decode())
    assert resp.status_code == 401
    assert "Invalid token. Please log in again." in data["message"]
    assert "fail" in data["status"]
    assert resp.content_type == "application/json"
