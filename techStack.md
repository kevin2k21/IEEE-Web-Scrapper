# IEEE Opportunities Scraper — Tech Stack

## Project Goal

Build a scraping and storage pipeline that:

1. Scrapes IEEE and IEEE CS websites for opportunities (calls for papers, conferences, scholarships, grants, fellowships, competitions, events)
2. Normalizes the extracted data into a consistent schema
3. Stores structured records in PostgreSQL
4. Deduplicates repeated opportunities
5. Exposes a basic REST API to query stored data

> **Scope:** Scraping + storage + API only. No LLM integration. No frontend. No notifications.

---

## Language

**Python 3.12+**

---

## Scraping

| Need | Library |
|---|---|
| Static HTML / RSS feeds | `requests` + `BeautifulSoup4` + `lxml` |
| JS-rendered pages | `Playwright` (Chromium) |
| Async HTTP requests | `httpx` |

Install:

```bash
pip install requests beautifulsoup4 lxml playwright httpx
playwright install chromium
```

Use `requests` + `BeautifulSoup4` first. Only reach for `Playwright` when a page requires JavaScript rendering.

---

## Database

**PostgreSQL**

Hosted locally via Docker during development. Use **Neon** or **Supabase** for production.

---

## ORM & Migrations

| Tool | Purpose |
|---|---|
| `SQLAlchemy 2.0` | Models, queries, session management |
| `Alembic` | Schema versioning and migrations |

Install:

```bash
pip install sqlalchemy psycopg2-binary alembic
```

---

## Data Validation

**Pydantic v2**

Used for normalizing and validating scraped data before writing to the database.

Install:

```bash
pip install pydantic
```

---

## API Layer

**FastAPI** + **Uvicorn**

Exposes endpoints to search, filter, and paginate stored opportunities.

Install:

```bash
pip install fastapi uvicorn
```

Run:

```bash
uvicorn app.main:app --reload
```

---

## Scheduling

**APScheduler**

Runs scraping jobs on a recurring schedule (e.g. every 6 hours).

Install:

```bash
pip install apscheduler
```

---

## Utilities

| Tool | Purpose |
|---|---|
| `loguru` | Structured logging and scraper debugging |
| `python-dotenv` | Environment variables and secrets |

Install:

```bash
pip install loguru python-dotenv
```

---

## Containerization

**Docker + Docker Compose**

Required for consistent local development and production deployment.

`docker-compose.yml` should define:
- `app` service (Python scraper + FastAPI)
- `db` service (PostgreSQL)

---

## Project Structure

```
project-root/
│
├── app/
│   ├── api/
│   │   └── routes/            # FastAPI route handlers
│   │
│   ├── core/
│   │   ├── config.py          # Settings, env vars
│   │   ├── logging.py         # Loguru setup
│   │   └── constants.py
│   │
│   ├── database/
│   │   ├── models/            # SQLAlchemy models
│   │   ├── session.py         # DB session factory
│   │   └── migrations/        # Alembic migration files
│   │
│   ├── scrapers/
│   │   ├── ieee/              # IEEE.org scraper
│   │   └── ieee_cs/           # IEEE CS scraper
│   │
│   ├── parsers/
│   │   ├── normalization/     # Clean + normalize raw data
│   │   ├── deduplication/     # Prevent duplicate records
│   │   └── extraction/        # Field extraction logic
│   │
│   ├── scheduler/
│   │   └── jobs.py            # APScheduler job definitions
│   │
│   └── main.py                # FastAPI app entrypoint
│
├── tests/
├── docker/
├── requirements.txt
├── docker-compose.yml
├── alembic.ini
└── .env
```

---

## Data Flow

```
[ APScheduler ]
      ↓
[ Scrapers — requests/BS4 or Playwright ]
      ↓
[ Parsers — normalize, deduplicate, validate with Pydantic ]
      ↓
[ PostgreSQL — via SQLAlchemy ]
      ↓
[ FastAPI — search, filter, paginate ]
```

---

## Opportunity Schema (Core Fields)

```python
class Opportunity(Base):
    id: int                      # Primary key
    source_url: str              # Where it was scraped from
    title: str
    category: str                # e.g. "conference", "scholarship", "grant"
    description: str
    deadline: date | None
    start_date: date | None
    organizer: str | None
    tags: list[str]              # JSON array
    raw_html: str | None         # Optional: store raw for reprocessing
    hash: str                    # SHA-256 of title+url for deduplication
    created_at: datetime
    updated_at: datetime
```

---

## Deduplication Strategy

Generate a `hash` field from a combination of `title` + `source_url` (SHA-256). On insert, check if the hash already exists. If it does, update the record instead of creating a duplicate.

---

## Development Phases

### Phase 1 — Foundation
- Single scraper (one IEEE source)
- PostgreSQL connection
- Normalized schema + Alembic migration
- Basic insert + deduplication

### Phase 2 — Multi-Source Scraping
- Add remaining IEEE / IEEE CS sources
- Async scraping with `httpx`
- APScheduler for periodic runs

### Phase 3 — API Layer
- FastAPI search endpoint
- Filtering by category, deadline, tags
- Pagination and sorting

---

## Dependencies Summary (`requirements.txt`)

```
requests
beautifulsoup4
lxml
playwright
httpx
sqlalchemy
psycopg2-binary
alembic
pydantic
fastapi
uvicorn
apscheduler
loguru
python-dotenv
```

---

## Explicitly Out of Scope (for now)

- LLM / AI enrichment (no OpenAI, Gemini, LangChain)
- Frontend (no Next.js)
- Email / notification system
- Vector databases or semantic search
- Kubernetes, Kafka, Selenium
- User accounts or authentication
