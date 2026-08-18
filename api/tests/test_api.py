from collections.abc import Generator

from fastapi.testclient import TestClient
from sqlalchemy import create_engine, func, select
from sqlalchemy.orm import Session, sessionmaker
from sqlalchemy.pool import StaticPool

from app.database import Base, get_db
from app.main import app
from app.models import Lead


def test_health_and_classification_persistence() -> None:
    test_engine = create_engine(
        "sqlite://",
        connect_args={"check_same_thread": False},
        poolclass=StaticPool,
    )
    testing_session = sessionmaker(bind=test_engine, expire_on_commit=False)
    Base.metadata.create_all(bind=test_engine)

    def override_get_db() -> Generator[Session, None, None]:
        with testing_session() as session:
            yield session

    app.dependency_overrides[get_db] = override_get_db
    client = TestClient(app)
    payload = {
        "name": "Carlos Silva",
        "email": "carlos@example.com",
        "phone": "11999999999",
        "insurance_type": "saude_empresarial",
        "message": (
            "Preciso de uma cotação urgente para minha empresa com 25 funcionários "
            "ainda hoje."
        ),
    }

    try:
        assert client.get("/health").json() == {"status": "ok"}

        response = client.post("/api/leads/classify", json=payload)

        assert response.status_code == 201
        assert response.json()["priority"] == "HIGH"
        with testing_session() as session:
            assert session.scalar(select(func.count()).select_from(Lead)) == 1
    finally:
        app.dependency_overrides.clear()
        test_engine.dispose()


def test_rejects_invalid_lead() -> None:
    client = TestClient(app)

    response = client.post(
        "/api/leads/classify",
        json={"name": "A", "email": "invalid", "message": ""},
    )

    assert response.status_code == 422
