from app.models import User


def test_password_hashing():
    user = User(username="alice", email="alice@example.com")
    user.set_password("my-password")

    assert user.password_hash != "my-password"
    assert user.check_password("my-password")
    assert not user.check_password("different-password")
