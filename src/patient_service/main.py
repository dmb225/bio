from fastapi import FastAPI, Depends
from sqlalchemy.orm import Session

from schemas import TestResult
from core.interfaces.database import get_db
from core.services.database import get_results, get_result_historic
from core.services.subscriber import get_subscriber

RESULT_TOPIC = "results"

app = FastAPI()


def background_task():
    print("Waiting for test results from laboratory_service...")
    subscriber = get_subscriber(RESULT_TOPIC)
    subscriber.subscribe()


@app.on_event("startup")
def startup_event():
    import threading
    task = threading.Thread(target=background_task)
    task.start()


@app.get("/patient/{patient_id}/results", response_model=list[TestResult])
def results(patient_id: int, db: Session = Depends(get_db)):
    print("main")
    print(db)
    return get_results(db=db, patient_id=patient_id)


@app.get("/patient/{patient_id}/result_historic/{test_name}", response_model=list[TestResult])
def result_historic(patient_id: int, test_name: str, db: Session = Depends(get_db)):
    return get_result_historic(db=db, patient_id=patient_id, test_name=test_name)


@app.get("/")
def root():
    return "Hello Patient"
