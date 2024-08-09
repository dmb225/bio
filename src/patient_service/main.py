import json
import os

from fastapi import FastAPI, Depends
from sqlalchemy.orm import Session
from database import get_db
from schemas import TestResult
from services import get_all_tests, get_test_historic, record_test
import redis

app = FastAPI()

# Initialize Redis
redis_client = redis.StrictRedis(
    host=os.getenv("REDIS_HOST", "localhost"),
    port=int(os.getenv("REDIS_PORT", 6379)),
    db=int(os.getenv("REDIS_DB", 8))
)

pubsub = redis_client.pubsub()
pubsub.subscribe('test_results_channel')


def background_task():
    print("Waiting for messages...")
    for message in pubsub.listen():
        print(f"New message received: {message}")  # Debugging line to see all messages
        if message['type'] == 'message':
            record_test(json.loads(message["data"]))


@app.on_event("startup")
def startup_event():
    import threading
    task = threading.Thread(target=background_task)
    task.start()


@app.get("/patient/{patient_id}/all_tests", response_model=list[TestResult])
def test_result(patient_id: int, db: Session = Depends(get_db)):
    return get_all_tests(db=db, patient_id=patient_id)


@app.get("/patient/{patient_id}/test_historic/{test_name}", response_model=list[TestResult])
def test_result(patient_id: int, test_name: str, db: Session = Depends(get_db)):
    return get_test_historic(db=db, patient_id=patient_id, test_name=test_name)


@app.get("/")
def root():
    return "Hello Patient"
