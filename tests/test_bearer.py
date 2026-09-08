"""
Bearer token authentication tests.
"""
VALID_TOKEN = "EDU-BEARER-2026"
INVALID_TOKEN = "WRONG-TOKEN"

HEADERS_VALID = {"Authorization": f"Bearer {VALID_TOKEN}"}
HEADERS_INVALID = {"Authorization": f"Bearer {INVALID_TOKEN}"}


def test_bearer_valid(client):
    r = client.get("/api/v1/bearer/students", headers=HEADERS_VALID)
    assert r.status_code == 200


def test_bearer_invalid(client):
    r = client.get("/api/v1/bearer/students", headers=HEADERS_INVALID)
    assert r.status_code == 401


def test_bearer_missing(client):
    r = client.get("/api/v1/bearer/students")
    assert r.status_code == 401


def test_bearer_error_structure(client):
    r = client.get("/api/v1/bearer/students", headers=HEADERS_INVALID)
    body = r.json()
    assert "detail" in body
    assert "error" in body["detail"]
    assert "code" in body["detail"]["error"]


def test_bearer_student_not_found(client):
    r = client.get("/api/v1/bearer/students/999999", headers=HEADERS_VALID)
    assert r.status_code == 404


def test_bearer_performance(client):
    r = client.get("/api/v1/bearer/academic-performance", headers=HEADERS_VALID)
    assert r.status_code == 200


def test_bearer_attendance(client):
    r = client.get("/api/v1/bearer/attendance", headers=HEADERS_VALID)
    assert r.status_code == 200


def test_bearer_examinations(client):
    r = client.get("/api/v1/bearer/examinations", headers=HEADERS_VALID)
    assert r.status_code == 200
