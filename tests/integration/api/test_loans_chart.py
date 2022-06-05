from fastapi.testclient import TestClient
from sqlalchemy.orm import Session

from balanced_backend.config import settings


def test_api_get_loans_chart(db: Session, client: TestClient):
    response = client.get(
        f"{settings.REST_PREFIX}/loans-chart?start_timestamp=1654409623&end_timestamp=1664409623&time_interval=84600")
    assert response.status_code == 200


def test_api_get_loans_chart_error(db: Session, client: TestClient):
    response = client.get(f"{settings.REST_PREFIX}/loans-chart?start_time=0")
    assert response.status_code == 400
