from pydantic import BaseModel, ConfigDict
from datetime import datetime


class ResultCreate(BaseModel):
    lab_name: str
    patient_id: int
    test_name: str
    result_date: datetime
    result_value: float
    unit: str


class Result(ResultCreate):
    id: int

    model_config = ConfigDict(from_attributes=True)
