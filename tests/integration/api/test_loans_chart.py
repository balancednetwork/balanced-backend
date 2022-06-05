from fastapi.testclient import TestClient
from sqlalchemy.orm import Session

from balanced_backend.config import settings


def test_api_get_loans_chart(db: Session, client: TestClient):
    response = client.get(f"{settings.REST_PREFIX}/preps")
    assert response.status_code == 200


def test_api_get_loans_chart_error(db: Session, client: TestClient):
    response = client.get(f"{settings.REST_PREFIX}?start_time=0")
    assert response.status_code == 204
