# NextGen Institute Educational ERP API

A centralized, publicly accessible Educational ERP REST API for  
**NextGen Institute of AI & Technology (NGIAT)**.

Built as a controlled external data source for testing the **Audit Assistant** REST/OpenAPI connector — specifically for validating REST ingestion, authentication detection, schema discovery, pagination, filtering, and relational data ingestion.

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
    │
    │  Internal network
    ▼
Render PostgreSQL   (nextgen-edu-db)
    │
    └── Synthetic educational dataset
        (50,000 – 100,000 students, ~several million records)
```

- **No direct database access from the internet.**  
- PostgreSQL is accessible only through the FastAPI application.  
- The only public interface is the FastAPI REST API over HTTPS.

---

## Technology Stack

| Layer       | Technology                              |
|-------------|----------------------------------------|
| Language    | Python 3.11+                           |
| Framework   | FastAPI                                |
| Server      | Uvicorn                                |
| ORM         | SQLAlchemy 2.x                         |
| Database    | PostgreSQL (Render Managed)            |
| Driver      | psycopg (v3)                           |
| Validation  | Pydantic v2                            |
| Config      | pydantic-settings + `.env`             |
| Data gen    | Faker (en_IN locale)                   |
| Tests       | pytest + httpx (SQLite in-memory)      |
| Deployment  | Render Web Service + Render PostgreSQL |

---

## Institution

| Field            | Value                                    |
|------------------|------------------------------------------|
| Name             | NextGen Institute of AI & Technology     |
| Short name       | NGIAT                                    |
| Institution code | NGIAT001                                 |
| City             | Pune, Maharashtra, India                 |
| Established      | 2005                                     |
| Accreditation    | NAAC A+                                  |

**Version 1** represents a single institution.  
The `institution_id` foreign-key architecture is preserved so multi-institution support can be added in a future version without redesigning the schema.

### Departments (8)

| Short | Department                                |
|-------|-------------------------------------------|
| CSE   | Computer Science & Engineering            |
| AIDS  | Artificial Intelligence & Data Science    |
| IT    | Information Technology                    |
| ECE   | Electronics & Communication Engineering   |
| EE    | Electrical Engineering                    |
| MECH  | Mechanical Engineering                    |
| CIVIL | Civil Engineering                         |
| BSH   | Basic Sciences & Humanities               |

---

## Authentication

| Mode        | Header            | Value / Credentials      | Route prefix        |
|-------------|-------------------|--------------------------|---------------------|
| No Auth     | —                 | —                        | `/api/v1/public/`   |
| Bearer      | `Authorization`   | `Bearer <BEARER_TOKEN>`  | `/api/v1/bearer/`   |
| API Key     | `X-API-Key`       | `<API_KEY>`              | `/api/v1/apikey/`   |
| HTTP Basic  | `Authorization`   | Basic `<b64(user:pass)>` | `/api/v1/basic/`    |

All credentials come from environment variables — never hardcoded.  
Invalid or missing credentials return **HTTP 401**.

---

## API Endpoints

### Health (no auth)
```
GET /              Root — API identity
GET /health        Database health check (SELECT 1) — used by Render and UptimeRobot
```

### Public (no auth)
```
GET /api/v1/public/institution     NGIAT institution record (singular)
GET /api/v1/public/institutions    Paginated list (future multi-institution)
GET /api/v1/public/campuses
GET /api/v1/public/departments
GET /api/v1/public/programs
GET /api/v1/public/courses
GET /api/v1/public/faculty
```

### Bearer Auth
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

### API Key Auth
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

All collection endpoints:

```
GET /api/v1/bearer/students?page=1&limit=100
```

Max `limit`: 1000. Response:

```json
{
  "data": [...],
  "pagination": { "page": 1, "limit": 100, "total": 50000, "total_pages": 500 }
}
```

## Filtering & Search

```
?department_id=1&batch_year=2024&status=active&gender=Female
?search=Aarav           (matches name, UID, roll number)
?sort=batch_year&order=desc
```

---

## Environment Variables

Copy `.env.example` → `.env` and fill in values. **Never commit `.env`.**

| Variable            | Description                                        | Example / Default            |
|---------------------|----------------------------------------------------|------------------------------|
| `APP_NAME`          | API display name                                   | `NextGen Institute...`       |
| `APP_VERSION`       | Semantic version                                   | `1.0.0`                      |
| `INSTITUTION_NAME`  | Full institution name                              | `NextGen Institute of AI...` |
| `INSTITUTION_SHORT` | Short code                                         | `NGIAT`                      |
| `SERVICE_NAME`      | Render service name                                | `nextgen-edu-api`            |
| `ENVIRONMENT`       | `development` or `production`                      | `development`                |
| `DATABASE_URL`      | PostgreSQL connection string                       | see `.env.example`           |
| `BEARER_TOKEN`      | Bearer token secret                                | `EDU-BEARER-2026-TEST`       |
| `API_KEY`           | API key secret                                     | `EDU-APIKEY-2026-TEST`       |
| `BASIC_USERNAME`    | Basic auth username                                | `audit_admin`                |
| `BASIC_PASSWORD`    | Basic auth password                                | `EduPassword@2026`           |
| `LOG_LEVEL`         | Python logging level                               | `INFO`                       |
| `DATASET_SIZE`      | Seed size: `small/medium/large/xl`                 | `medium`                     |
| `SEED_STUDENTS`     | Exact student count (overrides `DATASET_SIZE`)     | `0` (disabled)               |

---

## Local Development

```powershell
# 1. Clone and enter project
git clone https://github.com/<your-org>/educational-erp-api.git
cd educational-erp-api

# 2. Create virtual environment
python -m venv .venv
.venv\Scripts\activate

# 3. Install dependencies
pip install -r requirements.txt

# 4. Configure environment
copy .env.example .env
# Edit .env — set DATABASE_URL to your local PostgreSQL

# 5. Create schema
python scripts/01_create_schema.py

# 6. Seed master data (NGIAT institution, departments, programs)
python scripts/02_seed_master.py

# 7. Seed faculty
python scripts/03_seed_faculty.py

# 8. Seed courses
python scripts/04_seed_courses.py

# 9. Seed students (medium = 10,000 by default)
python scripts/05_seed_students.py

# 10. Seed academic records
python scripts/06_seed_academics.py

# 11. Seed career data
python scripts/07_seed_career.py

# 12. Validate dataset integrity
python scripts/08_validate_dataset.py

# 13. Run locally
uvicorn app.main:app --reload --port 8000
```

Open http://localhost:8000/docs for the Swagger UI.

### Dataset size control

```powershell
# PowerShell
$env:DATASET_SIZE="large";  python scripts/05_seed_students.py   # 50,000 students
$env:SEED_STUDENTS=100000;  python scripts/05_seed_students.py   # exactly 100,000
```

---

## Render Deployment

### Prerequisites
- GitHub account with this repo pushed to `main`
- Render account (https://render.com)

### Step 1 — Create PostgreSQL database

1. In Render dashboard → **New** → **PostgreSQL**
2. Name: `nextgen-edu-db`
3. Choose region (e.g. Oregon `us-west-2`)
4. Choose plan (Starter or above for persistent storage)
5. After creation, copy the **Internal Connection String**

### Step 2 — Create Web Service

1. In Render dashboard → **New** → **Web Service**
2. Connect your GitHub repo
3. Settings:
   - Name: `nextgen-edu-api`
   - Runtime: Python
   - Build command: `pip install -r requirements.txt`
   - Start command: `uvicorn app.main:app --host 0.0.0.0 --port $PORT`
   - Health check path: `/health`
4. Environment Variables (set as **Secret**):

   | Key              | Value                                              |
   |------------------|----------------------------------------------------|
   | `DATABASE_URL`   | Internal Connection String from `nextgen-edu-db`   |
   | `BEARER_TOKEN`   | Your production bearer secret                      |
   | `API_KEY`        | Your production API key secret                     |
   | `BASIC_USERNAME` | `audit_admin` (or your choice)                     |
   | `BASIC_PASSWORD` | Strong production password                         |
   | `ENVIRONMENT`    | `production`                                       |

5. Deploy — Render will build and start the service.

### Step 3 — Initialize database on Render

After the first successful deploy, run seed scripts targeting the Render database:

```powershell
# Set DATABASE_URL to the Render EXTERNAL connection string temporarily
$env:DATABASE_URL="postgresql+psycopg://user:password@dpg-xxx.oregon-postgres.render.com/nextgen_edu_db"

python scripts/01_create_schema.py
python scripts/02_seed_master.py
python scripts/03_seed_faculty.py
python scripts/04_seed_courses.py

# Production: seed 100,000 students
$env:SEED_STUDENTS=100000
python scripts/05_seed_students.py

python scripts/06_seed_academics.py
python scripts/07_seed_career.py
python scripts/08_validate_dataset.py
```

> **Important:** Seeding is an explicit one-time operation.  
> FastAPI does **not** re-seed on restart.  
> PostgreSQL on Render is persistent — data survives redeployments.

### Step 4 — Verify deployment

```
GET https://nextgen-edu-api.onrender.com/
GET https://nextgen-edu-api.onrender.com/health
GET https://nextgen-edu-api.onrender.com/docs
GET https://nextgen-edu-api.onrender.com/openapi.json
GET https://nextgen-edu-api.onrender.com/api/v1/public/institution
GET https://nextgen-edu-api.onrender.com/api/v1/bearer/students   (Authorization: Bearer <token>)
```

---

## UptimeRobot Setup

UptimeRobot provides **external availability monitoring** — it tells you when the service goes down.

> **Important distinction:**  
> UptimeRobot is an availability monitor, not a keep-alive mechanism.  
> Render's `/health` check is the service health mechanism.  
> If continuous uptime without sleeping is required, use a Render **paid plan** instead of relying on ping-based workarounds.

### Configuration steps

1. Log in to [UptimeRobot](https://uptimerobot.com)
2. Click **Add New Monitor**
3. Settings:
   - Monitor type: **HTTP(s)**
   - Friendly name: `NextGen Educational ERP API`
   - URL: `https://nextgen-edu-api.onrender.com/health`
   - Monitoring interval: 5 minutes (or as appropriate)
4. Save the monitor
5. Verify it reports **HTTP 200** — the `/health` endpoint returns 200 when PostgreSQL is reachable

The `/health` endpoint:
- Executes `SELECT 1` against PostgreSQL
- Returns `200` with `{"status": "healthy", "database": "healthy"}` when healthy
- Returns `503` with `{"status": "unhealthy", "database": "unavailable"}` when the database is unreachable
- Never queries large tables
- Never requires authentication

---

## Audit Assistant Integration

The deployed API is designed as an external REST data source for the Audit Assistant.

| Property         | Value                                                    |
|------------------|----------------------------------------------------------|
| Base URL         | `https://nextgen-edu-api.onrender.com`                   |
| OpenAPI          | `https://nextgen-edu-api.onrender.com/openapi.json`      |
| Swagger UI       | `https://nextgen-edu-api.onrender.com/docs`              |

### Authentication test matrix

| Test               | Expected |
|--------------------|----------|
| Public endpoint    | 200      |
| Bearer — valid     | 200      |
| Bearer — invalid   | 401      |
| Bearer — missing   | 401      |
| API key — valid    | 200      |
| API key — invalid  | 401      |
| API key — missing  | 401      |
| Basic — valid      | 200      |
| Basic — invalid    | 401      |
| Basic — missing    | 401      |

### What the Audit Assistant can test

- Discover the OpenAPI specification at `/openapi.json`
- Detect all 4 authentication schemes from `securitySchemes`
- Connect with No Auth, Bearer, API Key, and Basic Auth independently
- Retrieve paginated educational records
- Ingest relational data (students → performance, attendance, placements)
- Test pagination, filtering, search, sorting
- Validate authentication enforcement (401 on wrong/missing credentials)

---

## Running Tests

Tests use an in-memory SQLite database — no live PostgreSQL required.

```powershell
pytest
```

Test coverage:
- `test_health.py` — root and health endpoints
- `test_public.py` — public endpoints, no auth
- `test_bearer.py` — Bearer valid/invalid/missing, student endpoints
- `test_apikey.py` — API key valid/invalid/missing
- `test_basic.py` — Basic auth valid/invalid/missing
- `test_pagination.py` — pagination, sorting, filter validation

---

## Dataset Targets (Production)

| Entity                  | Target      |
|-------------------------|-------------|
| Institutions            | 1           |
| Campuses                | 2           |
| Departments             | 8           |
| Programs                | 15          |
| Courses                 | 1,000–2,000 |
| Faculty                 | 500–1,000   |
| **Students**            | **50,000–100,000** |
| Enrollments             | 300,000–600,000 |
| Academic Performance    | 300,000–600,000 |
| Attendance              | 1,000,000+  |
| Examinations            | 500,000+    |
| Placements              | 15,000–30,000 |
| Internships             | 20,000+     |
| Higher Studies          | 10,000+     |
| Entrepreneurship        | 2,000+      |
| Projects                | 50,000+     |
| Certifications          | 30,000+     |
| Publications            | 10,000+     |
| Professional Activities | 50,000+     |
| Awards                  | 5,000+      |

Build up progressively: start with `DATASET_SIZE=small` locally, then `DATASET_SIZE=xl` on Render.

---

## Security Notes

- All credentials loaded from environment variables — never hardcoded
- `.env` excluded from Git (`.gitignore` includes `.env` and `.env.*`)
- Authorization headers are never logged
- Sort/filter columns validated against whitelists (prevents ORDER BY injection)
- All DB queries use SQLAlchemy ORM (parameterized — no raw string interpolation)
- Internal stack traces not returned to API clients
- HTTPS enforced on Render (all HTTP redirects to HTTPS automatically)

---

## Troubleshooting

| Symptom | Likely cause | Fix |
|---------|-------------|-----|
| `/health` returns 503 | Database unreachable | Check `DATABASE_URL`; verify Render PostgreSQL is running |
| 401 on valid credentials | Wrong env var loaded | Confirm `.env` or Render env vars match your request headers |
| Empty responses after seeding | Wrong `DATABASE_URL` during seed | Re-seed using Render external connection string |
| Render deploy fails | Dependency issue | Check build logs; ensure `requirements.txt` has pinned versions |
| `No NGIAT master data found` | Seed order wrong | Run scripts in order: 01 → 02 → 03 → 04 → 05 → 06 → 07 |
| Duplicate seed data | Script ran twice without guard | Scripts are idempotent — re-running is safe but check counts |
