"""
Public endpoints — no auth, should always return 200.
"""


def test_institution_singular(client):
    """New /institution (singular) endpoint for NGIAT single-institution view."""
    r = client.get("/api/v1/public/institution")
    # 200 if seeded, 404 if no data — both are correct API behaviour in tests
    assert r.status_code in (200, 404)


def test_institutions_no_auth(client):
    r = client.get("/api/v1/public/institutions")
    assert r.status_code == 200
    body = r.json()
    assert "data" in body
    assert "pagination" in body


def test_campuses(client):
    r = client.get("/api/v1/public/campuses")
    assert r.status_code == 200


def test_departments(client):
    r = client.get("/api/v1/public/departments")
    assert r.status_code == 200


def test_programs(client):
    r = client.get("/api/v1/public/programs")
    assert r.status_code == 200


def test_courses(client):
    r = client.get("/api/v1/public/courses")
    assert r.status_code == 200


def test_faculty(client):
    r = client.get("/api/v1/public/faculty")
    assert r.status_code == 200


def test_pagination_meta(client):
    r = client.get("/api/v1/public/institutions?page=1&limit=10")
    body = r.json()
    meta = body["pagination"]
    assert meta["page"] == 1
    assert meta["limit"] == 10
