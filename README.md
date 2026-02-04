# Business CRUD API

A simple FastAPI project providing CRUD operations for a `Business` entity.

Features
- RESTful endpoints for create, read, update, partial update (PATCH), and delete
- PostgreSQL persistence via SQLAlchemy
- Router-based structure: `routers/business.py`
- Pydantic models in `models.py`
- Database configuration in `config.py`

Quickstart

1. Copy `.env.example` to `.env` and update the `DATABASE_URL` with your Postgres credentials.

2. Create the PostgreSQL database (example using psql):

```bash
psql -U postgres -c "CREATE DATABASE business_db;"
```

3. Activate your virtual environment and install dependencies (if not already):

```bash
G:/fastapi/venv/Scripts/Activate.ps1    # on Windows PowerShell
python -m pip install -r requirements.txt
```

If you don't have a `requirements.txt`, install:

```bash
python -m pip install fastapi uvicorn sqlalchemy psycopg2-binary python-dotenv
```

4. Start the application (auto-creates tables via SQLAlchemy `create_all`):

```bash
uvicorn main:app --reload
```

5. Open docs in your browser:
- Swagger UI: `http://127.0.0.1:8000/docs`
- ReDoc: `http://127.0.0.1:8000/redoc`

Project Layout

- [main.py](main.py) — App entrypoint and router registration
- [models.py](models.py) — Pydantic models (`Business`, `BusinessCreate`, `BusinessUpdate`)
- [config.py](config.py) — SQLAlchemy engine, `SessionLocal`, and `Base`
- [db_models.py](db_models.py) — SQLAlchemy ORM models
- [database.py](database.py) — Database CRUD operations using SQLAlchemy sessions
- [routers/business.py](routers/business.py) — APIRouter with business endpoints
- [.env.example](.env.example) — Example environment variables

Endpoints (summary)
- `POST /businesses/` — Create business
- `GET /businesses/` — List businesses (supports `skip`, `limit`, `industry` filters)
- `GET /businesses/{id}` — Retrieve one
- `PUT /businesses/{id}` — Full update
- `PATCH /businesses/{id}` — Partial update
- `DELETE /businesses/{id}` — Delete
- `GET /businesses/stats/overview` — Basic statistics

Notes & Next Steps
- This project uses `Base.metadata.create_all(bind=engine)` to create tables automatically. For production or schema migrations, use Alembic.
- Keep secrets out of the repository; use environment variables or a secrets manager.

If you want, I can also:
- Add a `requirements.txt`
- Add Alembic migrations
- Add basic tests or a small Postman collection

