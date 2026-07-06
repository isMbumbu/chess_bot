from fastapi.testclient import TestClient

from chess_bot.main import app


def test_health_check() -> None:
    with TestClient(app) as client:
        response = client.get("/health")

    assert response.status_code == 200
    assert response.json() == {"status": "ok"}


def test_analysis_returns_legal_move() -> None:
    with TestClient(app) as client:
        response = client.post("/api/v1/analysis/move", json={"fen": "startpos"})

    assert response.status_code == 200
    assert response.json()["move"] is not None
