Daily Updates
21st April 2026
Initialized The Project

22nd April 2026

## Implemented Chapter 1-5
- Flask application factory
- App configuration with `Config`
- SQLite database setup
- SQLAlchemy integration
- Flask-Migrate integration
- Flask-Login integration
- User registration
- User login
- User logout
- Remember Me login option
- Protected home route with `@login_required`
- Flash messages
- Password hashing and password verification
- Username uniqueness validation
- Email uniqueness validation
- User loader for Flask-Login
- Base template layout
- Home page template
- Login page template
- Registration page template
- Hardcoded sample posts on home page
- Database migrations for `user` table
- Database migrations for `post` table
- Basic automated tests

## Routes
- `/`
- `/index`
- `/login`
- `/logout`
- `/register`

## Forms
### `LoginForm`
- `username`
- `password`
- `remember_me`
- `submit`

### `RegistrationForm`
- `username`
- `email`
- `password`
- `password2`
- `submit`

## Models
### `User`
- `id`
- `username`
- `email`
- `password_hash`
- `posts`
- `set_password()`
- `check_password()`

### `Post`
- `id`
- `body`
- `timestamp`
- `user_id`
- `author`

## Templates
- `app/templates/base.html`
- `app/templates/index.html`
- `app/templates/login.html`
- `app/templates/register.html`

## Files Used In Main App
- `microblog.py`
- `config.py`
- `app/__init__.py`
- `app/forms.py`
- `app/models.py`
- `app/routes.py`
- `app/templates/`
- `migrations/`
- `tests/`

## Tests Present
- `tests/test_models.py`
- `tests/test_routes.py`
- `tests/test_auth.py`
- `tests/conftest.py`
