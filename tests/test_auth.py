import sqlalchemy as sa

from app import db
from app.models import User


def test_register_creates_user(client, app):
    response = client.post(
        "/auth/register",
        data={
            "username": "susan",
            "password": "cat",
            "password2": "cat",
        },
        follow_redirects=True,
    )

    assert b"Congratulations, you are now a registered user!" in response.data

    with app.app_context():
        user = db.session.scalar(sa.select(User).where(User.username == "susan"))
        assert user is not None
        assert user.check_password("cat")


def test_register_rejects_duplicate_username(client):
    response = client.post(
        "/auth/register",
        data={
            "username": "test",
            "password": "cat",
            "password2": "cat",
        },
    )

    assert b"Please use a different username." in response.data


def test_login_logout_flow(client, auth):
    response = auth.login(follow_redirects=True)
    assert b"Hi, test!" in response.data
    assert b"Logout" in response.data

    response = auth.logout(follow_redirects=False)
    assert response.status_code == 302
    assert response.headers["Location"].endswith("/index")


def test_invalid_login_shows_error(client):
    response = client.post(
        "/auth/login",
        data={"username": "test", "password": "wrong"},
        follow_redirects=True,
    )

    assert b"Invalid username or password" in response.data


def test_password_reset_request_redirects_to_reset_page(client):
    response = client.post(
        "/auth/reset_password_request",
        data={"username": "test"},
        follow_redirects=False,
    )

    assert response.status_code == 302
    assert "/auth/reset_password/" in response.headers["Location"]


def test_password_reset_request_unknown_user_flashes(client):
    response = client.post(
        "/auth/reset_password_request",
        data={"username": "nobody"},
        follow_redirects=True,
    )

    assert response.status_code == 200
    assert b"No account with that username." in response.data


def test_password_reset_flow_updates_password(client, app):
    with app.app_context():
        user = db.session.scalar(sa.select(User).where(User.username == "test"))
        token = user.get_reset_password_token()

    response = client.post(
        f"/auth/reset_password/{token}",
        data={"password": "newpw", "password2": "newpw"},
        follow_redirects=True,
    )

    assert b"Your password has been reset." in response.data

    with app.app_context():
        user = db.session.scalar(sa.select(User).where(User.username == "test"))
        assert user.check_password("newpw")


def test_authenticated_user_cannot_open_auth_pages(client, auth):
    auth.login()

    login_response = client.get("/auth/login")
    register_response = client.get("/auth/register")

    assert login_response.status_code == 302
    assert login_response.headers["Location"].endswith("/index")
    assert register_response.status_code == 302
    assert register_response.headers["Location"].endswith("/index")
