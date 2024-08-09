from sqlalchemy.orm import Session
from models import TestResultModel
from schemas import TestResultCreate


def create_test_result(db: Session, test_result: TestResultCreate):
    db_test_result = TestResultModel(**test_result.model_dump())
    db.add(db_test_result)
    db.commit()
    db.refresh(db_test_result)
    return db_test_result
