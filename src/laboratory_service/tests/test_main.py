import pytest
from fastapi.testclient import TestClient
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from ..database import Base, get_db
from ..main import app


# Setup for the test database
SQLALCHEMY_DATABASE_URL = "sqlite:///./bio_lab_test.db"
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


def test_record_test_result(setup_database):
    response = client.post("/record-test-result/", json={
        "patient_id": 1,
        "test_name": "Hemoglobin",
        "result_value": 13.5,
        "unit": "g/dL",
        "test_date": "2024-08-09T00:00:00Z",
        "lab_name": "LabCorp"
    })
    assert response.status_code == 201
    assert response.json()["test_name"] == "Hemoglobin"
    assert response.json()["result_value"] == 13.5


def test_record_test_result_invalid_data(setup_database):
    response = client.post("/record-test-result/", json={
        "patient_id": "invalid",
        "test_name": "Hemoglobin",
        "result_value": "not_a_float",
        "unit": "g/dL",
        "test_date": "invalid_date",
        "lab_name": "LabCorp"
    })
    assert response.status_code == 422
