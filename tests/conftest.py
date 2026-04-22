import os
import tempfile

import pytest

from app import create_app, db
from app.models import User


@pytest.fixture
def app():
    db_fd, db_path = tempfile.mkstemp()
    os.close(db_fd)

    app = create_app(
        test_config={
            "TESTING": True,
            "WTF_CSRF_ENABLED": False,
            "SQLALCHEMY_DATABASE_URI": f"sqlite:///{db_path}",
        }
    )

    with app.app_context():
        db.create_all()
        user = User(username="test", email="test@example.com")
        user.set_password("test")
        db.session.add(user)
        db.session.commit()

    yield app

    with app.app_context():
        db.session.remove()
        db.drop_all()
        db.engine.dispose()

    os.unlink(db_path)


@pytest.fixture
def client(app):
    return app.test_client()


@pytest.fixture
def runner(app):
    return app.test_cli_runner()


class AuthActions:
    def __init__(self, client):
        self._client = client

    def login(self, username="test", password="test", follow_redirects=False):
        return self._client.post(
            "/login",
            data={"username": username, "password": password},
            follow_redirects=follow_redirects,
        )

    def logout(self, follow_redirects=False):
        return self._client.get("/logout", follow_redirects=follow_redirects)


@pytest.fixture
def auth(client):
    return AuthActions(client)
