from sqlalchemy.orm import Session

from src.laboratory_service.models import ResultModel
from src.laboratory_service.schemas import ResultCreate


def create_result(db: Session, result_create: ResultCreate):
    db_result = ResultModel(**result_create.model_dump())
    db.add(db_result)
    db.commit()
    db.refresh(db_result)
    return db_result
