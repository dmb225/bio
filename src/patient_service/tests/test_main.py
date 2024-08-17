import datetime
import pytest
from pathlib import Path
from fastapi.testclient import TestClient
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

from src.patient_service.main import app
from src.patient_service.models import ResultModel
from src.patient_service.core.interfaces.database import Base, get_db

TEST_DB_PATH = Path(__file__).resolve().parent / "bio_patient_test.db"
SQLALCHEMY_DATABASE_URL = f"sqlite:///{TEST_DB_PATH}"
engine = create_engine(SQLALCHEMY_DATABASE_URL, connect_args={"check_same_thread": False})
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)


# Override get_db dependency to use the test database
def override_get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


app.dependency_overrides[get_db] = override_get_db
client = TestClient(app)


@pytest.fixture(scope="module")
def setup_database():
    Base.metadata.create_all(bind=engine)
    yield
    Base.metadata.drop_all(bind=engine)


def test_get_test_results(setup_database):
    patient_id = 1
    with SessionLocal() as db:
        db.add_all([
            ResultModel(
                patient_id=patient_id,
                test_name="Hemoglobin",
                result_value=13.5,
                unit="g/dL",
                result_date=datetime.datetime(year=2024, month=8, day=9),
                lab_name="Cerballiance"
            ),
            ResultModel(
                patient_id=patient_id,
                test_name="Hemoglobin",
                result_value=14.0,
                unit="g/dL",
                result_date=datetime.datetime(year=2024, month=8, day=10),
                lab_name="Cerballiance"
            )
        ])
        db.commit()

    response = client.get(f"/patient/{patient_id}/results")
    payload = response.json()

    assert response.status_code == 200
    assert len(payload) == 2
    assert payload[0]["test_name"] == "Hemoglobin"
    assert payload[0]["result_value"] == 13.5
