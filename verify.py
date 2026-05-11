"""
Smoke-test harness for the Microblog Flask Mega-Tutorial project.

Run from project root with the venv active:

    python verify.py

It enumerates every route registered by create_app() and exercises each one
via the Flask test client. With real dependencies installed it will also report
a richer set of status codes than the offline sandbox can.
"""
from app import create_app

app = create_app(test_config={
    "TESTING": True,
    "SECRET_KEY": "verify-only",
    "WTF_CSRF_ENABLED": False,
    "ELASTICSEARCH_URL": None,
    "POSTS_PER_PAGE": 25,
    "SERVER_NAME": "localhost",
})

print(f"Blueprints: {sorted(app.blueprints)}")
print(f"Rules: {len(list(app.url_map.iter_rules()))}\n")

client = app.test_client()

# Each row: (method, url, set_of_acceptable_status_codes, label)
checks = [
    ("GET",    "/",                                  {200, 302}, "main.index"),
    ("GET",    "/index",                             {200, 302}, "main.index alias"),
    ("GET",    "/explore",                           {200, 302}, "main.explore"),
    ("GET",    "/auth/login",                        {200},      "auth.login GET"),
    ("GET",    "/auth/register",                     {200},      "auth.register GET"),
    ("GET",    "/auth/logout",                       {302},      "auth.logout"),
    ("GET",    "/auth/reset_password_request",       {200},      "reset_password_request GET"),
    ("GET",    "/auth/reset_password/sometoken",     {200, 302}, "reset_password GET"),
    ("GET",    "/edit_profile",                      {200, 302}, "edit_profile"),
    ("GET",    "/user/test",                         {200, 302, 404}, "user profile"),
    ("GET",    "/user/test/popup",                   {200, 302, 404}, "user popup"),
    ("GET",    "/messages",                          {200, 302}, "messages"),
    ("GET",    "/search?q=hi",                       {200, 302}, "search"),
    ("GET",    "/export_posts",                      {200, 302}, "export_posts"),
    ("GET",    "/notifications?since=0",             {200, 302}, "notifications"),
    ("POST",   "/translate",                         {200, 302, 400}, "translate"),
    ("POST",   "/follow/test",                       {200, 302, 404}, "follow"),
    ("POST",   "/unfollow/test",                     {200, 302, 404}, "unfollow"),
    ("POST",   "/send_message/test",                 {200, 302, 404}, "send_message"),
    ("GET",    "/api/users",                         {200, 401},      "api.get_users"),
    ("GET",    "/api/users/1",                       {200, 401, 404}, "api.get_user"),
    ("GET",    "/api/users/1/followers",             {200, 401, 404}, "api.get_followers"),
    ("GET",    "/api/users/1/following",             {200, 401, 404}, "api.get_following"),
    ("POST",   "/api/users",                         {201, 400, 415}, "api.create_user"),
    ("POST",   "/api/tokens",                        {200, 401},      "api.get_token"),
    ("DELETE", "/api/tokens",                        {204, 401},      "api.revoke_token"),
    ("GET",    "/this-route-does-not-exist",         {404},           "404 handler"),
]

ok = 0
for method, url, expected, label in checks:
    try:
        if method == "GET":
            r = client.get(url)
        elif method == "POST":
            r = client.post(url, json={} if url.startswith("/api") or url == "/translate" else None,
                            data={} if "follow" in url or "message" in url else None)
        elif method == "PUT":
            r = client.put(url, json={})
        elif method == "DELETE":
            r = client.delete(url)
        passed = r.status_code in expected
        if passed:
            ok += 1
        marker = "PASS" if passed else "FAIL"
        print(f"  {marker}  {method:6s} {url:42s} -> {r.status_code}  ({label})")
    except Exception as e:
        print(f"  EXC   {method:6s} {url:42s} -> {type(e).__name__}: {e}")

print(f"\n{ok}/{len(checks)} routes returned an expected status code")
