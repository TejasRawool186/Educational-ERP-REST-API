"""
HTTP Basic authentication tests.
"""
import base64

def basic_header(username, password):
    token = base64.b64encode(f"{username}:{password}".encode()).decode()
    return {"Authorization": f"Basic {token}"}


VALID = basic_header("audit_admin", "EduPassword@2026")
INVALID = basic_header("wrong_user", "wrong_pass")


def test_basic_valid(client):
    r = client.get("/api/v1/basic/students", headers=VALID)
    assert r.status_code == 200


def test_basic_invalid(client):
    r = client.get("/api/v1/basic/students", headers=INVALID)
    assert r.status_code == 401


def test_basic_missing(client):
    r = client.get("/api/v1/basic/students")
    assert r.status_code == 401


def test_basic_placements(client):
    r = client.get("/api/v1/basic/placements", headers=VALID)
    assert r.status_code == 200


def test_basic_higher_studies(client):
    r = client.get("/api/v1/basic/higher-studies", headers=VALID)
    assert r.status_code == 200


def test_basic_entrepreneurship(client):
    r = client.get("/api/v1/basic/entrepreneurship", headers=VALID)
    assert r.status_code == 200


def test_basic_publications(client):
    r = client.get("/api/v1/basic/publications", headers=VALID)
    assert r.status_code == 200


def test_basic_professional_activities(client):
    r = client.get("/api/v1/basic/professional-activities", headers=VALID)
    assert r.status_code == 200


def test_basic_awards(client):
    r = client.get("/api/v1/basic/awards", headers=VALID)
    assert r.status_code == 200
