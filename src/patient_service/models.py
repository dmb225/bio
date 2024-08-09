from sqlalchemy import Column, Integer, String, Float, DateTime
from database import Base, engine


class TestResultModel(Base):
    __tablename__ = "test_results"

    id = Column(Integer, primary_key=True, index=True)
    patient_id = Column(Integer, index=True)
    test_name = Column(String, index=True)
    result_value = Column(Float)
    unit = Column(String)
    test_date = Column(DateTime)
    lab_name = Column(String)


# Create the database tables
Base.metadata.create_all(bind=engine)
