from fastapi.testclient import TestClient

from src import api


client = TestClient(api.app)


def test_health_endpoint_returns_online_status():
    response = client.get("/health")
    assert response.status_code == 200
    assert response.json()["status"] == "online"


def test_unknown_user_is_rejected():
    response = client.post(
        "/validate-access",
        json={"user_id": "missing-user", "app_id": "demo"},
    )
    assert response.status_code == 404
    assert response.json()["detail"] == "Usuário não encontrado"


def test_minor_access_is_denied_during_curfew(monkeypatch):
    monkeypatch.setattr(api, "is_curfew_active", lambda: True)
    response = client.post(
        "/validate-access",
        json={"user_id": "user123", "app_id": "demo"},
    )
    assert response.status_code == 200
    assert response.json()["allowed"] is False


def test_access_is_allowed_outside_curfew(monkeypatch):
    monkeypatch.setattr(api, "is_curfew_active", lambda: False)
    response = client.post(
        "/validate-access",
        json={"user_id": "user123", "app_id": "demo"},
    )
    assert response.status_code == 200
    assert response.json()["allowed"] is True
