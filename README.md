# StreamFlow

StreamFlow is a deliberately small event storage API. Its first version receives,
validates, stores, and retrieves events using FastAPI, SQLAlchemy, and PostgreSQL.

## Project structure

```text
app/
├── handlers/
│   ├── payment_handlers.py # Business logic for payment events
│   └── user_handlers.py    # Business logic for user events
├── __init__.py          # Makes app a Python package
├── database.py          # Database engine, sessions, and session dependency
├── main.py              # Application startup and HTTP endpoints
├── models.py            # SQLAlchemy Event table mapping
├── processor.py         # Selects, dispatches, and updates one event
└── schemas.py           # Pydantic request and response shapes
```

## Run locally

You need Python 3.11+ and a running PostgreSQL server. Create the database once:

```bash
createdb streamflow
```

Then install and start the API:

```bash
python -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
export DATABASE_URL="postgresql+psycopg://postgres:postgres@localhost:5432/streamflow"
uvicorn app.main:app --reload
```

The `events` table is created when the application starts. Interactive API docs
are available at <http://127.0.0.1:8000/docs>.

## Try the API

Create an event:

```bash
curl -X POST http://127.0.0.1:8000/events \
  -H "Content-Type: application/json" \
  -d '{"event_type":"user.created","source":"accounts-api","payload":{"user_id":123,"email":"alice@example.com"}}'
```

Retrieve events:

```bash
curl http://127.0.0.1:8000/events
curl http://127.0.0.1:8000/events/1
```

Process the oldest pending event:

```bash
curl -X POST http://127.0.0.1:8000/events/process-next
```

Retry a failed event, filter events, or view status counts:

```bash
curl -X POST http://127.0.0.1:8000/events/1/retry
curl 'http://127.0.0.1:8000/events?status=failed&event_type=payment.completed'
curl http://127.0.0.1:8000/events/stats
```

## Intentional limitations

- `create_all()` creates missing tables but cannot safely evolve an existing
  schema. A migration tool can be introduced when the model first needs to change.
- Listing returns every event. Pagination can wait until the growing result set
  creates a real problem.
- Database work is synchronous. That keeps the request-to-SQL flow visible; an
  async driver can wait until concurrency requirements justify the added concepts.
- There are no workers, queues, retries, authentication, Docker setup, or frontend.
