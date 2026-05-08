# Microblog

Flask Mega-Tutorial project completed through Chapter 23.

## Included Features

- Application factory, blueprints, configuration, logging, and CLI commands
- Database models and migrations for users, posts, followers, messages, notifications, tasks, and API tokens
- Registration, login, logout, remember-me sessions, and password reset email flow
- User profiles, avatars, edit profile, following/unfollowing, pagination, and private messages
- Post creation, language detection, search integration, translation endpoint, and moment.js timestamps
- Email support, background export jobs with Redis/RQ, Docker/deployment files, and REST API endpoints

## Chapter Coverage

1. Hello World: Flask entry point and app factory
2. Templates: base and page templates
3. Web Forms: Flask-WTF forms
4. Database: SQLAlchemy models and migrations
5. User Logins: Flask-Login auth flow
6. Profile Page and Avatars: user pages and Gravatar
7. Error Handling: HTML and JSON error handlers
8. Followers: follower association table and routes
9. Pagination: index, explore, user, search, and messages pagination
10. Email Support: email helpers and password reset templates
11. Facelift: Bootstrap 5 templates
12. Dates and Times: Flask-Moment integration
13. I18n and L10n: Flask-Babel, translation CLI, Spanish catalog
14. Ajax: translation endpoint
15. Better Application Structure: auth/main/errors/api blueprints
16. Full-Text Search: Elasticsearch search hooks
17. Deployment on Linux: supervisor/nginx deployment files
18. Deployment on Heroku: Procfile
19. Deployment on Docker: Dockerfile and boot script
20. JavaScript Magic: user popovers and client-side helpers
21. User Notifications: unread-message and task notifications
22. Background Jobs: Redis/RQ task queue and post export
23. Application Programming Interfaces: REST API and token auth

## Setup

```powershell
venv\Scripts\python -m pip install -e ".[test]"
venv\Scripts\flask db upgrade
venv\Scripts\flask translate compile
```

## Run

```powershell
venv\Scripts\flask run
```

Open `http://127.0.0.1:5000`.

## Test

```powershell
venv\Scripts\python -m pytest
```

The local SQLite database `app.db` has already been upgraded to the final chapter-23 schema.
