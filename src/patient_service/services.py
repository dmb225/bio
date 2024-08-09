from datetime import datetime

from fastapi import HTTPException, status
from sqlalchemy import desc
from sqlalchemy.orm import Session

from database import SessionLocal
from models import TestResultModel
from exceptions import DatabaseError


def get_all_tests(db: Session, patient_id: int):
    return db.query(TestResultModel).filter(TestResultModel.patient_id == patient_id).order_by(desc(TestResultModel.test_date)).all()


def get_test_historic(db: Session, patient_id: int, test_name: str):
    try:
        return db.query(TestResultModel).filter(TestResultModel.patient_id == patient_id, TestResultModel.test_name == test_name).order_by(desc(TestResultModel.test_date)).all()
    except DatabaseError as e:
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail="Internal Server Error")
    except Exception as e:
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail="Unexpected error occurred")


def record_test(test: dict) -> None:
    new_test_result = TestResultModel(
        patient_id=test['patient_id'],
        test_name=test['test_name'],
        result_value=test['result_value'],
        unit=test['unit'],
        test_date=datetime.fromisoformat(test['test_date'].replace("Z", "+00:00")),
        lab_name=test['lab_name']
    )

    db = SessionLocal()
    db.add(new_test_result)
    db.commit()
    db.close()
