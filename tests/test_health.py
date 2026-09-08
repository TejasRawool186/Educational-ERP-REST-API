def test_root(client):
    r = client.get("/")
    assert r.status_code == 200
    body = r.json()
    assert body["status"] == "operational"
    assert "documentation" in body
    assert "institution" in body
    assert "NextGen" in body["institution"]


def test_health_returns_200_or_503(client):
    """
    /health must return 200 (DB reachable) or 503 (DB unavailable).
    In the test environment with SQLite the DB is always reachable.
    """
    r = client.get("/health")
    assert r.status_code in (200, 503)
    body = r.json()
    assert "status" in body
    assert "database" in body
    assert "service" in body
    assert "version" in body


def test_health_structure(client):
    r = client.get("/health")
    body = r.json()
    # service name must reflect NGIAT branding
    assert body["service"] == "nextgen-edu-api"


def test_health_no_auth_required(client):
    """Health endpoint must be publicly accessible — no auth headers."""
    r = client.get("/health")
    assert r.status_code != 401
    assert r.status_code != 403
