import pytest
from fastapi.testclient import TestClient
from sqlalchemy import create_engine, text
from sqlalchemy.orm import sessionmaker
from ..database import Base, get_db
from ..main import app

# Setup for the test database
SQLALCHEMY_DATABASE_URL = "sqlite:///./bio_test.db"
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
    # Insert a test result
    db = SessionLocal()
    db.execute(
        text("INSERT INTO test_results (patient_id, test_name, result_value, unit, test_date, lab_name) "
             "VALUES (:patient_id, :test_name, :result_value, :unit, :test_date, :lab_name)"),
        {"patient_id": 1, "test_name": "Hemoglobin", "result_value": 13.5, "unit": "g/dL",
         "test_date": "2024-08-09T00:00:00Z", "lab_name": "Cerballiance"}
    )
    db.execute(
        text("INSERT INTO test_results (patient_id, test_name, result_value, unit, test_date, lab_name) "
             "VALUES (:patient_id, :test_name, :result_value, :unit, :test_date, :lab_name)"),
        {"patient_id": 1, "test_name": "Hemoglobin", "result_value": 14.0, "unit": "g/dL",
         "test_date": "2024-08-10T00:00:00Z", "lab_name": "Cerballiance"}
    )
    db.commit()
    db.close()

    response = client.get("/test-results/1")
    payload = response.json()

    assert response.status_code == 200
    assert len(payload) == 2
    assert payload[0]["test_name"] == "Hemoglobin"
    assert payload[0]["result_value"] == 13.5

