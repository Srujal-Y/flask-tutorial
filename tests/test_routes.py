def test_index_requires_login(client):
    response = client.get("/", follow_redirects=False)

    assert response.status_code == 302
    assert "/login?next=%2F" in response.headers["Location"]


def test_index_renders_for_logged_in_user(client, auth):
    response = auth.login(follow_redirects=True)

    assert b"Beautiful day in Portland!" in response.data
    assert b"The Avengers movie was so cool!" in response.data
