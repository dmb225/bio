from pydantic import BaseModel, ConfigDict
from datetime import datetime


class TestResult(BaseModel):
    id: int
    lab_name: str
    patient_id: int
    test_name: str
    result_date: datetime
    result_value: float
    unit: str

    model_config = ConfigDict(from_attributes=True)
