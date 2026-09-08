"""
API key header authentication tests.
"""
VALID_KEY = "EDU-APIKEY-2026"
INVALID_KEY = "WRONG-KEY"

HEADERS_VALID = {"X-API-Key": VALID_KEY}
HEADERS_INVALID = {"X-API-Key": INVALID_KEY}


def test_apikey_valid(client):
    r = client.get("/api/v1/apikey/students", headers=HEADERS_VALID)
    assert r.status_code == 200


def test_apikey_invalid(client):
    r = client.get("/api/v1/apikey/students", headers=HEADERS_INVALID)
    assert r.status_code == 401


def test_apikey_missing(client):
    r = client.get("/api/v1/apikey/students")
    assert r.status_code == 401


def test_apikey_faculty(client):
    r = client.get("/api/v1/apikey/faculty", headers=HEADERS_VALID)
    assert r.status_code == 200


def test_apikey_enrollments(client):
    r = client.get("/api/v1/apikey/enrollments", headers=HEADERS_VALID)
    assert r.status_code == 200


def test_apikey_courses(client):
    r = client.get("/api/v1/apikey/courses", headers=HEADERS_VALID)
    assert r.status_code == 200


def test_apikey_internships(client):
    r = client.get("/api/v1/apikey/internships", headers=HEADERS_VALID)
    assert r.status_code == 200


def test_apikey_projects(client):
    r = client.get("/api/v1/apikey/projects", headers=HEADERS_VALID)
    assert r.status_code == 200


def test_apikey_certifications(client):
    r = client.get("/api/v1/apikey/certifications", headers=HEADERS_VALID)
    assert r.status_code == 200
