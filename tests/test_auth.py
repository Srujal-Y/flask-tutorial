import sqlalchemy as sa

from app import db
from app.models import User


def test_register_creates_user(client, app):
    response = client.post(
        "/register",
        data={
            "username": "susan",
            "email": "susan@example.com",
            "password": "cat",
            "password2": "cat",
        },
        follow_redirects=True,
    )

    assert b"Congratulations, you are now a registered user!" in response.data

    with app.app_context():
        user = db.session.scalar(sa.select(User).where(User.username == "susan"))
        assert user is not None
        assert user.email == "susan@example.com"
        assert user.check_password("cat")


def test_register_rejects_duplicate_username(client):
    response = client.post(
        "/register",
        data={
            "username": "test",
            "email": "new@example.com",
            "password": "cat",
            "password2": "cat",
        },
    )

    assert b"Please use a different username." in response.data


def test_register_rejects_duplicate_email(client):
    response = client.post(
        "/register",
        data={
            "username": "new-user",
            "email": "test@example.com",
            "password": "cat",
            "password2": "cat",
        },
    )

    assert b"Please use a different email address." in response.data


def test_login_logout_flow(client, auth):
    response = auth.login(follow_redirects=True)
    assert b"Hi, test!" in response.data
    assert b"Logout" in response.data

    response = auth.logout(follow_redirects=False)
    assert response.status_code == 302
    assert response.headers["Location"].endswith("/index")


def test_invalid_login_shows_error(client):
    response = client.post(
        "/login",
        data={"username": "test", "password": "wrong"},
        follow_redirects=True,
    )

    assert b"Invalid username or password" in response.data


def test_authenticated_user_cannot_open_auth_pages(client, auth):
    auth.login()

    login_response = client.get("/login")
    register_response = client.get("/register")

    assert login_response.status_code == 302
    assert login_response.headers["Location"].endswith("/index")
    assert register_response.status_code == 302
    assert register_response.headers["Location"].endswith("/index")
