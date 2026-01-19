# Namo

Baby name analytics and voting platform built with FastAPI, Vue 3, and PostgreSQL. Runs via a single Docker Compose stack.

## Stack

- FastAPI + SQLAlchemy
- Vue 3 + Vite + Tailwind CSS
- PostgreSQL
- Nginx (static frontend + API proxy)

## Quick start

1) Create secrets in `secrets/`:

- `secrets/prod_postgres_password.txt`
- `secrets/prod_secret_key.txt`
- `secrets/telegram_bot_token.txt`
- `secrets/prod_telegram_chat_id.txt`

2) Run:

```bash
docker compose up -d --build
```

3) Open:

- Frontend: http://localhost:8060
- API: http://localhost:8061
- Docs: http://localhost:8061/docs

## Data + seeding

The database is persistent via the `db-data-prod` volume. By default, startup does not seed data. To seed on startup, set `INIT_DB_ON_STARTUP=true` in the backend environment.

## Structure

```
app/       # backend + frontend
data/      # CSV data sources
nginx/     # nginx.conf
secrets/   # Docker secrets
docker-compose.yml
```
