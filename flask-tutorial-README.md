# Flask Tutorial Project — Implementation Checklist

This is the detailed per-feature checklist for the Microblog application built
through Chapter 23 of the Flask Mega-Tutorial. See `README.md` for the high-level
overview and run instructions.

## Local customization (deviation from canonical tutorial)

This project removes email from the user-facing flows:
- Registration asks for username + password only (no email field).
- Password reset asks for username only — entering a valid username redirects
  straight to the set-new-password page (no email is sent).
- `User.email` column is still present but nullable, so the rest of the code
  (Gravatar avatar, API serialization) still works; `User.avatar()` falls back
  to hashing the username when no email is set.
- API `POST /users` accepts `email` as an optional field; uniqueness is only
  checked when an email is provided.
- New Alembic migration `a1b2c3d4e5f6_make_email_nullable.py` flips the column.
- `app/auth/email.py`, `app/email.py`, and the email templates are left in
  place but unused for password resets, so the email feature can be re-wired
  later without rebuilding it.

Security note: anyone who knows a username can reset that account's password.
Fine for a local/learning project; do not deploy this version publicly.

## Chapters Implemented: 1 through 23

### Chapter 1 — Hello World
- `microblog.py` entry point with shell context processor
- `Config` class in `config.py` with env-var driven settings and `.env` loading

### Chapter 2 — Templates
- `app/templates/base.html` layout, page templates for index, user, etc.
- Jinja blocks, `{% extends %}` / `{% include %}` patterns

### Chapter 3 — Web Forms
- Flask-WTF forms in `app/auth/forms.py` and `app/main/forms.py`
- CSRF protection (via `SECRET_KEY`)
- `bootstrap_wtf.html` macro for Bootstrap-styled form rendering

### Chapter 4 — Database
- SQLAlchemy 2.x typed `Mapped[...]` models in `app/models.py`
- Alembic migrations in `migrations/versions/` (9 revisions, linear chain)
- `User` and `Post` models with relationship

### Chapter 5 — User Logins
- Flask-Login integration, `UserMixin`, `@login_required`
- Login / logout / register routes in `app/auth/routes.py`
- Password hashing via `werkzeug.security`
- Remember-me support, `next` query param redirect

### Chapter 6 — Profile Page and Avatars
- `/user/<username>` route and `user.html` template
- Gravatar via `User.avatar(size)` md5-hashed email
- `/edit_profile` route with `EditProfileForm`
- `last_seen` field updated in `before_app_request`

### Chapter 7 — Error Handling
- `app/errors/` blueprint with 404 and 500 handlers
- `RotatingFileHandler` for `logs/microblog.log`
- `SMTPHandler` for emailing admins on error
- Stdout logging path for containerized deployment

### Chapter 8 — Followers
- Self-referential `followers` association table
- `User.follow`, `unfollow`, `is_following`, `followers_count`, `following_count`
- `User.following_posts()` query (own + followed authors)
- `/follow/<username>` and `/unfollow/<username>` POST routes with `EmptyForm`

### Chapter 9 — Pagination
- `db.paginate` on index, explore, user, search, and messages
- `POSTS_PER_PAGE` config
- Newer / older navigation in templates

### Chapter 10 — Email Support
- `app/email.py` helpers (`send_email`, async via `Thread`)
- Password reset flow: `reset_password_request` and `reset_password` routes
- JWT-based reset tokens (`get_reset_password_token`, `verify_reset_password_token`)
- HTML and plain-text email templates

### Chapter 11 — Facelift (Bootstrap)
- Bootstrap 5.3 CSS/JS via CDN in `base.html`
- Responsive navbar, alerts, pagination
- `bootstrap_wtf.html` `quick_form` macro

### Chapter 12 — Dates and Times
- Flask-Moment integration (`moment.include_moment()`, `moment.lang(g.locale)`)
- `moment(timestamp).fromNow()` / `.format('LLL')` in templates

### Chapter 13 — I18n and L10n
- Flask-Babel integration with `_` and `lazy_gettext as _l`
- `babel.cfg` configuration
- Spanish translation catalog (`app/translations/es/LC_MESSAGES/messages.po` + `.mo`)
- CLI commands: `flask translate init`, `update`, `compile` (in `app/cli.py`)

### Chapter 14 — Ajax
- `/translate` POST endpoint
- Microsoft Translator integration in `app/translate.py`
- Client-side `translate(...)` async fetch in `base.html`
- Language auto-detection on new posts via `langdetect`

### Chapter 15 — A Better Application Structure
- Application factory `create_app(config_class, test_config)`
- Blueprints: `main`, `auth`, `errors`, `api`, `cli`
- Test-config injection for pytest

### Chapter 16 — Full-Text Search
- `app/search.py` with Elasticsearch index/delete/query helpers
- `SearchableMixin` on `Post` (auto-indexes on commit)
- `/search` route with `SearchForm` in `g`
- Graceful degradation when `ELASTICSEARCH_URL` is unset

### Chapter 17 — Deployment on Linux
- `deployment/supervisor/microblog.conf` (gunicorn)
- `deployment/supervisor/microblog-tasks.conf` (rq worker)
- `deployment/nginx/microblog` (http→https redirect, static alias)
- `Vagrantfile` for local VM provisioning

### Chapter 18 — Deployment on Heroku
- `Procfile` with web and worker dynos
- `DATABASE_URL` postgres scheme rewrite in `config.py`
- `LOG_TO_STDOUT` toggle

### Chapter 19 — Deployment with Docker
- `Dockerfile` (python:slim, gunicorn entrypoint)
- `boot.sh` (retry-loop migrations + gunicorn exec)

### Chapter 20 — JavaScript Magic
- User popovers via Bootstrap `Popover` in `base.html`
- `/user/<username>/popup` route and `user_popup.html`
- Hover-triggered async load with `popupLoaded` cache flag

### Chapter 21 — User Notifications
- `Notification` model
- `User.add_notification` (dedup-on-name)
- `/notifications` polling endpoint
- Unread-message badge in navbar with `set_message_count` JS
- Private messages: `Message` model, `/send_message/<recipient>`, `/messages` routes

### Chapter 22 — Background Jobs
- `Task` model
- Redis + RQ via `app.task_queue`
- `User.launch_task`, `get_tasks_in_progress`, `get_task_in_progress`
- `app/tasks.py` with `export_posts` job and `_set_task_progress`
- `/export_posts` route, progress notifications via `task_progress`

### Chapter 23 — Application Programming Interfaces
- `app/api/` blueprint (mounted at `/api`)
- `User.to_dict` / `from_dict` / `PaginatedAPIMixin`
- Endpoints: `GET/POST/PUT /users`, `GET /users/<id>`, followers/following
- HTTP basic auth (`/api/tokens` POST) and bearer-token auth (`/api/tokens` DELETE, all reads)
- JSON error responses, content-negotiating 404/500 handlers

## Routes Summary

### Main blueprint
- `GET/POST /` and `/index`
- `GET /explore`
- `GET /user/<username>`, `GET /user/<username>/popup`
- `GET/POST /edit_profile`
- `POST /follow/<username>`, `POST /unfollow/<username>`
- `POST /translate`
- `GET /search`
- `GET/POST /send_message/<recipient>`, `GET /messages`
- `GET /export_posts`
- `GET /notifications`

### Auth blueprint (`/auth` prefix)
- `GET/POST /login`, `GET /logout`, `GET/POST /register`
- `GET/POST /reset_password_request`, `GET/POST /reset_password/<token>`

### API blueprint (`/api` prefix)
- `GET /users`, `POST /users`, `GET /users/<id>`, `PUT /users/<id>`
- `GET /users/<id>/followers`, `GET /users/<id>/following`
- `POST /tokens`, `DELETE /tokens`

## Models

- `User` (auth, profile, followers, tokens, notification helpers, task helpers, API dict serialization)
- `Post` (`SearchableMixin`, language field)
- `Message` (sender, recipient, body, timestamp)
- `Notification` (name, payload_json, timestamp)
- `Task` (id from rq job, complete flag, progress reader)
- `followers` association table

## Tests

- `tests/conftest.py` — pytest fixtures (app, client, runner, AuthActions)
- `tests/test_models.py` — password hashing, gravatar URL
- `tests/test_auth.py` — register, login, logout, duplicate detection, password reset
- `tests/test_routes.py` — index, profile, edit profile, export_posts graceful failure, 404, last_seen update
- `tests/test_api.py` — token issuance, authenticated GET/PUT, unauthorized rejection
