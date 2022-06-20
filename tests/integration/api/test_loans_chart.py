from fastapi.testclient import TestClient
from sqlalchemy.orm import Session

from balanced_backend.config import settings


def test_api_get_loans_chart(db: Session, client: TestClient):
    """Test endpoint - must be run after one of the worker tests."""
    response = client.get(
        f"{settings.REST_PREFIX}/historical?address=cx66d4d90f5f113eba575bf793570135f9b10cece1")
    assert response.status_code == 200
    assert len(response.json()) > 0


def test_api_get_loans_chart_error(db: Session, client: TestClient):
    response = client.get(f"{settings.REST_PREFIX}/historical")
    assert response.status_code == 400
