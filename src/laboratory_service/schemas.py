from pydantic import BaseModel, ConfigDict
from datetime import datetime


class TestResultCreate(BaseModel):
    lab_name: str
    patient_id: int
    test_name: str
    test_date: datetime
    result_value: float
    unit: str


class TestResult(TestResultCreate):
    id: int

    model_config = ConfigDict(from_attributes=True)
