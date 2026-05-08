import base64

import sqlalchemy as sa

from app import db
from app.models import User


def _basic_auth(username, password):
    token = base64.b64encode(f"{username}:{password}".encode()).decode()
    return {"Authorization": f"Basic {token}"}


def _bearer_auth(token):
    return {"Authorization": f"Bearer {token}"}


def test_api_create_token_get_and_update_user(client, app):
    response = client.post(
        "/api/users",
        json={
            "username": "api-user",
            "email": "api-user@example.com",
            "password": "cat",
        },
    )

    assert response.status_code == 201
    assert response.json["username"] == "api-user"
    assert response.headers["Location"].endswith(f"/api/users/{response.json['id']}")

    token_response = client.post(
        "/api/tokens", headers=_basic_auth("api-user", "cat")
    )

    assert token_response.status_code == 200
    token = token_response.json["token"]

    get_response = client.get(
        f"/api/users/{response.json['id']}", headers=_bearer_auth(token)
    )

    assert get_response.status_code == 200
    assert "email" not in get_response.json
    assert get_response.json["username"] == "api-user"

    update_response = client.put(
        f"/api/users/{response.json['id']}",
        headers=_bearer_auth(token),
        json={"about_me": "Created through the API"},
    )

    assert update_response.status_code == 200
    assert update_response.json["about_me"] == "Created through the API"

    with app.app_context():
        user = db.session.scalar(sa.select(User).where(User.username == "api-user"))
        assert user.about_me == "Created through the API"


def test_api_rejects_protected_users_without_token(client):
    response = client.get("/api/users")

    assert response.status_code == 401
    assert response.json["error"] == "Unauthorized"
