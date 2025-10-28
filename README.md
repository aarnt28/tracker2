# Tracker2

Fresh scaffold using FastAPI + SQLAlchemy + Alembic + Jinja, containerized and ready for Zoraxy.

- **Port:** 9444
- **External domain:** https://tracker2.turnernet.co
- **Health:** `/health`
- **Metrics:** `/metrics`
- **API v1 ping:** `/api/v1/ping/` (requires `X-API-Key`)

## Quickstart (Docker)
```bash
cp .env.example .env
# set API_TOKEN and UI_PASSWORD_HASH (passlib bcrypt)
docker compose up -d --build
# http://localhost:9444/health