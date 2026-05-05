import pytest
from fastapi.testclient import TestClient
from sqlalchemy.pool import StaticPool
from sqlmodel import Session, SQLModel, create_engine

TEST_DATABASE_URL = "sqlite://"


@pytest.fixture(scope="function")
def test_engine():
    # Importar modelo para registrarlo en SQLModel.metadata
    from models.simulacion_db import Simulacion  # noqa: F401

    engine = create_engine(
        TEST_DATABASE_URL,
        connect_args={"check_same_thread": False},
        poolclass=StaticPool,
    )
    SQLModel.metadata.create_all(engine)
    yield engine
    SQLModel.metadata.drop_all(engine)


@pytest.fixture(scope="function")
def session(test_engine):
    with Session(test_engine) as s:
        yield s


@pytest.fixture(scope="function")
def client(session):
    from unittest.mock import patch

    from main import app
    from db.session import get_session

    def override_session():
        yield session

    app.dependency_overrides[get_session] = override_session

    # Evitar que el startup event intente conectar a PostgreSQL (no disponible en tests)
    with patch("db.session.init_engine"), TestClient(app, raise_server_exceptions=True) as c:
        yield c

    app.dependency_overrides.clear()
