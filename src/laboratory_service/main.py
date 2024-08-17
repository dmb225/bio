from fastapi import FastAPI, Depends, HTTPException, status
from sqlalchemy.orm import Session

from src.laboratory_service.schemas import ResultCreate, Result
from src.laboratory_service.exceptions import DatabaseError, ValidationError
from src.laboratory_service.core.interfaces.database import get_db
from src.laboratory_service.core.services.database import create_result
from src.laboratory_service.core.services.publisher import PublisherPort, get_publisher

app = FastAPI()


@app.post("/record_result/", response_model=Result, status_code=status.HTTP_201_CREATED)
def record_result(
        result_create: ResultCreate,
        db: Session = Depends(get_db),
        publisher: PublisherPort = Depends(get_publisher)
):
    try:
        result = create_result(db=db, result_create=result_create)
        message = {
            "patient_id": result.patient_id,
            "test_name": result.test_name,
            "result_value": result.result_value,
            "unit": result.unit,
            "result_date": result.result_date.isoformat(),
            "lab_name": result.lab_name
        }
        publisher.publish(message)

        return result
    except ValidationError as e:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=str(e))
    except DatabaseError as e:
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail="Internal Server Error")
    except Exception as e:
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail="Unexpected error occurred")


@app.get("/")
def root():
    return "Hello Laboratory"
