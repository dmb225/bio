import os
import redis
import json

from fastapi import FastAPI, Depends, HTTPException, status
from sqlalchemy.orm import Session

from schemas import TestResultCreate, TestResult
from database import get_db
from exceptions import DatabaseError, ValidationError
from services import create_test_result

app = FastAPI()

# Initialize Redis
redis_client = redis.StrictRedis(
    host=os.getenv("REDIS_HOST", "localhost"),
    port=int(os.getenv("REDIS_PORT", 6379)),
    db=int(os.getenv("REDIS_DB", 8))
)


@app.post("/record-test-result/", response_model=TestResult, status_code=status.HTTP_201_CREATED)
def record_test_result(test_result: TestResultCreate, db: Session = Depends(get_db)):
    try:
        result = create_test_result(db=db, test_result=test_result)

        # Publish the result to the Redis channel
        message = {
            "patient_id": result.patient_id,
            "test_name": result.test_name,
            "result_value": result.result_value,
            "unit": result.unit,
            "test_date": result.test_date.isoformat(),
            "lab_name": result.lab_name
        }
        print(message)
        redis_client.publish('test_results_channel', json.dumps(message))

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
