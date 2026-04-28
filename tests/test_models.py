from app.models import User


def test_password_hashing():
    user = User(username="alice", email="alice@example.com")
    user.set_password("my-password")

    assert user.password_hash != "my-password"
    assert user.check_password("my-password")
    assert not user.check_password("different-password")


def test_avatar_url():
    user = User(username="john", email="John@Example.com")

    assert user.avatar(128) == (
        "https://www.gravatar.com/avatar/"
        "d4c74594d841139328695756648b6bd6?d=identicon&s=128"
    )
