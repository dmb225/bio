from datetime import datetime
from fastapi import HTTPException, status
from sqlalchemy import desc
from sqlalchemy.orm import Session


from src.patient_service.core.interfaces.database import SessionLocal
from src.patient_service.exceptions import DatabaseError
from src.patient_service.models import ResultModel


def get_results(db: Session, patient_id: int):
    return (
        db.query(ResultModel)
        .filter(ResultModel.patient_id == patient_id)
        .order_by(desc(ResultModel.result_date)).all()
    )


def get_result_historic(db: Session, patient_id: int, test_name: str):
    try:
        return (
            db.query(ResultModel)
            .filter(ResultModel.patient_id == patient_id, ResultModel.test_name == test_name)
            .order_by(desc(ResultModel.result_date))
            .all()
        )
    except DatabaseError as e:
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail="Internal Server Error")
    except Exception as e:
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail="Unexpected error occurred")


def record_test(test: dict) -> None:
    new_test_result = ResultModel(
        patient_id=test['patient_id'],
        test_name=test['test_name'],
        result_value=test['result_value'],
        unit=test['unit'],
        result_date=datetime.fromisoformat(test['result_date'].replace("Z", "+00:00")),
        lab_name=test['lab_name']
    )

    db = SessionLocal()
    db.add(new_test_result)
    db.commit()
    db.close()
