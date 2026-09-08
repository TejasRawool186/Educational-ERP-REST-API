"""
Pagination and filtering tests.
"""
HEADERS = {"Authorization": "Bearer EDU-BEARER-2026"}


def test_default_pagination(client):
    r = client.get("/api/v1/bearer/students", headers=HEADERS)
    meta = r.json()["pagination"]
    assert meta["page"] == 1
    assert meta["limit"] == 100


def test_custom_pagination(client):
    r = client.get("/api/v1/bearer/students?page=2&limit=5", headers=HEADERS)
    assert r.status_code == 200
    meta = r.json()["pagination"]
    assert meta["page"] == 2
    assert meta["limit"] == 5


def test_limit_max_enforced(client):
    r = client.get("/api/v1/bearer/students?limit=9999", headers=HEADERS)
    # FastAPI should reject values > 1000 with 422
    assert r.status_code == 422


def test_pagination_structure(client):
    r = client.get("/api/v1/public/departments")
    body = r.json()
    meta = body["pagination"]
    assert "page" in meta
    assert "limit" in meta
    assert "total" in meta
    assert "total_pages" in meta


def test_sort_invalid_column(client):
    r = client.get("/api/v1/bearer/students?sort=invalid_col", headers=HEADERS)
    assert r.status_code == 400


def test_sort_valid(client):
    r = client.get("/api/v1/bearer/students?sort=batch_year&order=desc", headers=HEADERS)
    assert r.status_code == 200
