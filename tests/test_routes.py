from datetime import datetime

import sqlalchemy as sa

from app import db
from app.models import User


def test_index_requires_login(client):
    response = client.get("/", follow_redirects=False)

    assert response.status_code == 302
    assert "/login?next=%2F" in response.headers["Location"]


def test_index_renders_for_logged_in_user(client, auth):
    response = auth.login(follow_redirects=True)

    assert b"Beautiful day in Portland!" in response.data
    assert b"The Avengers movie was so cool!" in response.data


def test_user_profile_requires_login(client):
    response = client.get("/user/test", follow_redirects=False)

    assert response.status_code == 302
    assert "/login?next=%2Fuser%2Ftest" in response.headers["Location"]


def test_user_profile_renders_for_logged_in_user(client, auth):
    auth.login()
    response = client.get("/user/test")

    assert b"User: test" in response.data
    assert b"gravatar.com/avatar" in response.data
    assert b"Test post #1" in response.data
    assert b"Edit your profile" in response.data


def test_edit_profile_updates_current_user(client, auth, app):
    auth.login()
    response = client.post(
        "/edit_profile",
        data={"username": "renamed", "about_me": "Learning Flask"},
        follow_redirects=True,
    )

    assert b"Your changes have been saved." in response.data

    with app.app_context():
        user = db.session.scalar(sa.select(User).where(User.username == "renamed"))
        assert user is not None
        assert user.about_me == "Learning Flask"


def test_edit_profile_rejects_duplicate_username(client, auth, app):
    with app.app_context():
        user = User(username="susan", email="susan@example.com")
        user.set_password("cat")
        db.session.add(user)
        db.session.commit()

    auth.login()
    response = client.post(
        "/edit_profile",
        data={"username": "susan", "about_me": ""},
    )

    assert b"Please use a different username." in response.data


def test_last_seen_is_recorded_before_requests(client, auth, app):
    old_time = datetime(2000, 1, 1)
    with app.app_context():
        user = db.session.scalar(sa.select(User).where(User.username == "test"))
        user.last_seen = old_time
        db.session.commit()

    auth.login()
    client.get("/user/test")

    with app.app_context():
        user = db.session.scalar(sa.select(User).where(User.username == "test"))
        assert user.last_seen > old_time


def test_404_error_page(client):
    response = client.get("/does-not-exist")

    assert response.status_code == 404
    assert b"File Not Found" in response.data
