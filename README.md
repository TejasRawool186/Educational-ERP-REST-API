# NextGen Institute Educational ERP API

A centralized, publicly accessible Educational ERP REST API for  
**NextGen Institute of AI & Technology (NGIAT)**.

Built as a controlled external data source for testing the **Audit Assistant** REST/OpenAPI connector — specifically for validating REST ingestion, authentication detection, schema discovery, pagination, filtering, and relational data ingestion.

---

## Live URLs

| Resource | URL |
|----------|-----|
| Base API | https://nextgen-edu-api.onrender.com |
| Health Check | https://nextgen-edu-api.onrender.com/health |
| Swagger UI | https://nextgen-edu-api.onrender.com/docs |
| OpenAPI JSON | https://nextgen-edu-api.onrender.com/openapi.json |
| ReDoc | https://nextgen-edu-api.onrender.com/redoc |

---

## Architecture

```
Internet
    │
    ▼
Audit Assistant
    │  HTTPS / JSON
    ▼
Render Web Service  (nextgen-edu-api)
    │  Python 3.11 · FastAPI · Uvicorn
    │
    │  Internal network (Singapore region)
    ▼
Render PostgreSQL 16  (nextgen-edu-db)
    │
    └── Synthetic NGIAT educational dataset
        (4,000 students · ~570,000+ records)
```

- PostgreSQL is accessible **only** through the FastAPI application — never directly from the internet.
- The only public interface is the FastAPI REST API over HTTPS.
- Render handles TLS termination — all HTTP traffic is automatically redirected to HTTPS.

---

## Technology Stack

| Layer | Technology |
|-------|------------|
| Language | Python 3.11.9 (pinned via `.python-version`) |
| Framework | FastAPI 0.115.6 |
| Server | Uvicorn 0.32.1 |
| ORM | SQLAlchemy 2.0.36 |
| Database | PostgreSQL 16 (Render Managed — Singapore) |
| DB Driver | psycopg 3.2.3 (binary) |
| Validation | Pydantic 2.10.3 |
| Config | pydantic-settings 2.6.1 + `.env` |
| Data generation | Faker 33.1.0 (en_IN locale) |
| Tests | pytest 8.3.4 + httpx (SQLite in-memory) |
| Deployment | Render Web Service + Render PostgreSQL |
| Monitoring | UptimeRobot (Keyword monitor — GET /health) |

---

## Institution

| Field | Value |
|-------|-------|
| Name | NextGen Institute of AI & Technology |
| Short name | NGIAT |
| Institution code | NGIAT001 |
| Type | Autonomous Technical Institute |
| City | Pune, Maharashtra, India |
| Established | 2005 |
| Accreditation | NAAC A+ |
| Campuses | 1 (Main Campus, Hinjewadi) |

The `institution_id` foreign-key architecture is preserved so multi-institution support can be added in a future version without any schema changes.

---

## Departments (6)

| Code | Department |
|------|-----------|
| CSE | Computer Science & Engineering |
| AIDS | Artificial Intelligence & Data Science |
| IT | Information Technology |
| ECE | Electronics & Communication Engineering |
| MECH | Mechanical Engineering |
| BSH | Basic Sciences & Humanities |

---

## Programs (10)

| Code | Program | Degree | Duration |
|------|---------|--------|----------|
| BTECH-CSE | B.Tech Computer Science & Engineering | B.Tech | 4 years |
| MTECH-CE | M.Tech Computer Engineering | M.Tech | 2 years |
| BTECH-AIDS | B.Tech Artificial Intelligence & Data Science | B.Tech | 4 years |
| MTECH-AI | M.Tech Artificial Intelligence | M.Tech | 2 years |
| BTECH-IT | B.Tech Information Technology | B.Tech | 4 years |
| BTECH-ECE | B.Tech Electronics & Communication Engineering | B.Tech | 4 years |
| MTECH-ECE | M.Tech Electronics & Communication | M.Tech | 2 years |
| BTECH-MECH | B.Tech Mechanical Engineering | B.Tech | 4 years |
| MSC-MATH | M.Sc. Mathematics | M.Sc. | 2 years |
| MSC-PHY | M.Sc. Physics | M.Sc. | 2 years |

---

## Dataset (Production — Deployed)

| Table | Count |
|-------|------:|
| Institution | 1 |
| Campus | 1 |
| Departments | 6 |
| Programs | 10 |
| Faculty | 220 |
| Courses | 350 |
| **Students** | **4,000** |
| Enrollments | ~35,000 |
| Academic Performance | ~24,000 |
| Attendance | ~125,000 |
| Examinations | ~175,000 |
| Grades | ~175,000 |
| Internships | 1,800 |
| Placements | 1,500 |
| Higher Studies | 500 |
| Entrepreneurship | 150 |
| Projects | 3,500 |
| Certifications | 2,500 |
| Publications | 400 |
| Professional Activities | 5,000 |
| Awards | 650 |
| **Total records** | **~570,000+** |

All data is fully synthetic — no real personal information.  
Student emails follow `s######@ngiat.edu.in`, faculty emails follow `faculty#####@ngiat.edu.in`.

---

## Authentication

| Mode | Header | Credential | Route prefix |
|------|--------|------------|--------------|
| No Auth | — | — | `/api/v1/public/` |
| Bearer Token | `Authorization: Bearer <token>` | `BEARER_TOKEN` env var | `/api/v1/bearer/` |
| API Key | `X-API-Key: <key>` | `API_KEY` env var | `/api/v1/apikey/` |
| HTTP Basic | `Authorization: Basic <b64>` | `BASIC_USERNAME` + `BASIC_PASSWORD` env vars | `/api/v1/basic/` |

All credentials come from environment variables — never hardcoded.  
Invalid or missing credentials return **HTTP 401**.

---

## API Endpoints

### Health (no auth)
```
GET /              Root — NGIAT identity JSON
GET /health        Real DB health check (SELECT 1) — 200 healthy / 503 unavailable
```

### Public (no auth)
```
GET /api/v1/public/institution      NGIAT institution record (singular)
GET /api/v1/public/institutions     Paginated list (future multi-institution support)
GET /api/v1/public/campuses
GET /api/v1/public/departments
GET /api/v1/public/programs
GET /api/v1/public/courses
GET /api/v1/public/faculty
```

### Bearer Auth (`Authorization: Bearer <token>`)
```
GET /api/v1/bearer/students
GET /api/v1/bearer/students/{student_id}
GET /api/v1/bearer/students/{student_id}/performance
GET /api/v1/bearer/students/{student_id}/attendance
GET /api/v1/bearer/students/{student_id}/placements
GET /api/v1/bearer/students/{student_id}/internships
GET /api/v1/bearer/students/{student_id}/projects
GET /api/v1/bearer/academic-performance
GET /api/v1/bearer/attendance
GET /api/v1/bearer/examinations
```

### Bearer — Analytics
```
GET /api/v1/bearer/analytics/student-count
GET /api/v1/bearer/analytics/average-cgpa
GET /api/v1/bearer/analytics/placement-rate
GET /api/v1/bearer/analytics/average-package
GET /api/v1/bearer/analytics/department-performance
GET /api/v1/bearer/analytics/attendance-summary
GET /api/v1/bearer/analytics/higher-studies
```

### API Key Auth (`X-API-Key: <key>`)
```
GET /api/v1/apikey/students
GET /api/v1/apikey/faculty
GET /api/v1/apikey/enrollments
GET /api/v1/apikey/courses
GET /api/v1/apikey/internships
GET /api/v1/apikey/projects
GET /api/v1/apikey/certifications
```

### HTTP Basic Auth
```
GET /api/v1/basic/students
GET /api/v1/basic/placements
GET /api/v1/basic/higher-studies
GET /api/v1/basic/entrepreneurship
GET /api/v1/basic/publications
GET /api/v1/basic/professional-activities
GET /api/v1/basic/awards
```

---

## Pagination

All collection endpoints support pagination:

```
GET /api/v1/bearer/students?page=1&limit=100
```

Maximum `limit`: 1000. Response envelope:

```json
{
  "data": [...],
  "pagination": {
    "page": 1,
    "limit": 100,
    "total": 4000,
    "total_pages": 40
  }
}
```

## Filtering, Search & Sorting

```
# Filter
?department_id=1&batch_year=2023&status=active&gender=Female

# Search (matches full name, first name, last name, student UID, roll number)
?search=Aarav

# Sort
?sort=batch_year&order=desc
?sort=cgpa&order=asc
```

---

## Environment Variables

Copy `.env.example` → `.env` and fill in values. **Never commit `.env`.**

| Variable | Description | Default |
|----------|-------------|---------|
| `APP_NAME` | API display name | `NextGen Institute Educational ERP API` |
| `APP_VERSION` | Semantic version | `1.0.0` |
| `INSTITUTION_NAME` | Full institution name | `NextGen Institute of AI & Technology` |
| `INSTITUTION_SHORT` | Short code | `NGIAT` |
| `SERVICE_NAME` | Render service name | `nextgen-edu-api` |
| `ENVIRONMENT` | `development` or `production` | `development` |
| `DATABASE_URL` | PostgreSQL connection string | see `.env.example` |
| `BEARER_TOKEN` | Bearer token secret | `EDU-BEARER-2026-TEST` |
| `API_KEY` | API key secret | `EDU-APIKEY-2026-TEST` |
| `BASIC_USERNAME` | Basic auth username | `audit_admin` |
| `BASIC_PASSWORD` | Basic auth password | `EduPassword@2026` |
| `LOG_LEVEL` | Python logging level | `INFO` |
| `SEED_STUDENTS` | Exact student count for seeding | `4000` |

---

## Local Development

```powershell
# 1. Clone
git clone https://github.com/TejasRawool186/Educational-ERP-REST-API.git
cd Educational-ERP-REST-API

# 2. Virtual environment
python -m venv .venv
.venv\Scripts\activate

# 3. Install dependencies
pip install -r requirements.txt

# 4. Configure
copy .env.example .env
# Edit .env — set DATABASE_URL to your local PostgreSQL

# 5. Run locally
uvicorn app.main:app --reload --port 8000
```

Open http://localhost:8000/docs for Swagger UI.

---

## Database Seeding

### Seed order (must follow this sequence)

```powershell
# Set your DATABASE_URL first
$env:DATABASE_URL = "postgresql+psycopg://user:password@host/dbname"

# 0. Wipe existing data (type YES when prompted)
python scripts/00_wipe_database.py

# 1. Create all 21 tables
python scripts/01_create_schema.py

# 2. Master data: 1 institution, 1 campus, 6 departments, 10 programs
python scripts/02_seed_master.py

# 3. 220 faculty across 6 departments
python scripts/03_seed_faculty.py

# 4. 350 courses across departments and programs
python scripts/04_seed_courses.py

# 5. 4,000 students
python scripts/05_seed_students.py

# 6. Academic records (35k enrollments, 125k attendance, 175k exams/grades)
python scripts/06_seed_academics.py

# 7. Career data (placements, internships, projects, certifications, etc.)
python scripts/07_seed_career.py

# 8. Validate all 12 integrity checks
python scripts/08_validate_dataset.py
```

### Wipe and reseed (if needed)

The wipe script uses `DROP SCHEMA public CASCADE` to cleanly bypass the circular FK dependency between `departments` and `faculty`.

```powershell
python scripts/00_wipe_database.py   # type YES to confirm
python scripts/02_seed_master.py
# ... continue from step 3
```

All seed scripts are **idempotent** — they skip if data already exists.

---

## Render Deployment

### Services

| Service | Name | Region | Plan |
|---------|------|--------|------|
| Web Service | `nextgen-edu-api` | Singapore | Free |
| PostgreSQL 16 | `nextgen-edu-db` | Singapore | Free |

### Web Service settings

```
Runtime:       Python 3.11 (pinned via .python-version file)
Build command: pip install -r requirements.txt
Start command: uvicorn app.main:app --host 0.0.0.0 --port $PORT
Health check:  /health
```

### Required environment variables on Render

| Key | Value |
|-----|-------|
| `DATABASE_URL` | Internal Connection String from `nextgen-edu-db` (add `+psycopg` after `postgresql`) |
| `BEARER_TOKEN` | Your production bearer secret |
| `API_KEY` | Your production API key secret |
| `BASIC_USERNAME` | `audit_admin` |
| `BASIC_PASSWORD` | Strong production password |
| `ENVIRONMENT` | `production` |

### Seeding the Render database

After first deploy, run seed scripts from your local machine using the **External** connection string:

```powershell
$env:DATABASE_URL = "postgresql+psycopg://user:password@dpg-xxx.singapore-postgres.render.com/nextgen_edu_db"

python scripts/00_wipe_database.py   # if reseeding
python scripts/02_seed_master.py
python scripts/03_seed_faculty.py
python scripts/04_seed_courses.py
python scripts/05_seed_students.py
python scripts/06_seed_academics.py
python scripts/07_seed_career.py
python scripts/08_validate_dataset.py
```

> Seeding is a **one-time explicit operation**. FastAPI does not reseed on restart.  
> PostgreSQL on Render is persistent — data survives redeployments and service restarts.

---

## UptimeRobot Monitoring

UptimeRobot monitors external availability — it alerts you when the service goes down.

### Configuration

| Setting | Value |
|---------|-------|
| Monitor type | **Keyword monitoring** |
| Friendly name | NextGen Educational ERP API |
| URL | `https://nextgen-edu-api.onrender.com/health` |
| Keyword | `healthy` |
| Keyword condition | **Start incident when keyword is MISSING** |
| Interval | 5 minutes |
| Notification | Email |

> **Why Keyword monitoring?**  
> HTTP/website monitoring sends a HEAD request — FastAPI only accepts GET on `/health` and returns 405.  
> Keyword monitoring sends GET and also verifies the response body contains `"healthy"`,  
> which confirms both the application and PostgreSQL database are working.

### What `/health` returns

```json
// 200 OK — when healthy
{"status": "healthy", "service": "nextgen-edu-api", "version": "1.0.0", "database": "healthy"}

// 503 Service Unavailable — when database is unreachable
{"status": "unhealthy", "service": "nextgen-edu-api", "version": "1.0.0", "database": "unavailable"}
```

> **Note on Render free tier:** Services sleep after 15 minutes of inactivity.  
> UptimeRobot pings every 5 minutes so the service stays mostly awake,  
> but a ~30 second cold-start delay may occur after longer idle periods.  
> Use a Render **Starter plan ($7/mo)** to disable sleeping entirely.

---

## Running Tests

Tests use an in-memory SQLite database — no live PostgreSQL required.

```powershell
pytest
```

All 44 tests pass:

| File | Tests |
|------|-------|
| `test_health.py` | Root endpoint, health check structure, no-auth required |
| `test_public.py` | Public endpoints, /institution singular, pagination metadata |
| `test_bearer.py` | Bearer valid/invalid/missing, student CRUD, sub-resources |
| `test_apikey.py` | API key valid/invalid/missing, all apikey endpoints |
| `test_basic.py` | Basic auth valid/invalid/missing, all basic endpoints |
| `test_pagination.py` | Pagination, max limit enforcement, sort whitelist, sort order |

---

## Audit Assistant Integration

| Property | Value |
|----------|-------|
| Base URL | `https://nextgen-edu-api.onrender.com` |
| OpenAPI spec | `https://nextgen-edu-api.onrender.com/openapi.json` |
| Swagger UI | `https://nextgen-edu-api.onrender.com/docs` |

### Authentication test matrix

| Test | Expected |
|------|----------|
| Public endpoint (no auth) | 200 |
| Bearer — valid token | 200 |
| Bearer — invalid token | 401 |
| Bearer — missing header | 401 |
| API key — valid key | 200 |
| API key — invalid key | 401 |
| API key — missing header | 401 |
| Basic — valid credentials | 200 |
| Basic — wrong password | 401 |
| Basic — missing header | 401 |

### What the Audit Assistant can test

- Discover the OpenAPI specification at `/openapi.json`
- Detect all 4 authentication schemes from `securitySchemes` (BearerAuth, ApiKeyAuth, BasicAuth, plus public)
- Connect with No Auth, Bearer, API Key, and Basic Auth independently
- Retrieve paginated educational records across 21 tables
- Ingest relational data (students → performance, attendance, placements, internships, projects)
- Test pagination, filtering by department/batch/status, full-text search, safe sorting
- Validate that invalid and missing credentials are correctly rejected with 401

---

## Security

- All credentials loaded from environment variables — never hardcoded in source
- `.env` excluded from Git (`.gitignore` covers `.env` and `.env.*`)
- Authorization headers are never logged
- Sort/filter columns validated against per-model whitelists (prevents ORDER BY injection)
- All DB queries use SQLAlchemy ORM with parameterized expressions
- Internal stack traces are never returned to API clients
- HTTPS enforced on Render — HTTP is automatically redirected to HTTPS

---

## Troubleshooting

| Symptom | Likely cause | Fix |
|---------|-------------|-----|
| `/health` returns 503 | PostgreSQL unreachable | Check `DATABASE_URL`; verify `nextgen-edu-db` is running on Render |
| 401 on valid credentials | Wrong credential in request | Confirm your request headers match the env vars set in Render |
| UptimeRobot shows DOWN with 405 | Monitor type set to HTTP/website (sends HEAD) | Change to **Keyword monitoring** (sends GET) |
| UptimeRobot shows DOWN with keyword mismatch | Keyword condition set to "exists" | Change to **"keyword is MISSING"** |
| Empty API responses after seeding | Seeded against wrong DATABASE_URL | Re-run seed scripts with the Render external connection string |
| Render build fails (pydantic-core Rust error) | Render picked Python 3.14+ | `.python-version` file pins 3.11.9 — ensure it is committed |
| `CircularDependencyError` on wipe | SQLAlchemy can't sort departments↔faculty drop order | Use `00_wipe_database.py` — it uses `DROP SCHEMA CASCADE` |
| `No NGIAT master data found` | Seed scripts run out of order | Always run: 02 → 03 → 04 → 05 → 06 → 07 |
| Seed script skips with "already seeded" | Idempotency guard triggered | Run `00_wipe_database.py` first, then reseed from step 02 |
