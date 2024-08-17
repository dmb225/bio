from sqlalchemy import Column, Integer, String, Float, DateTime

from src.patient_service.core.interfaces.database import Base, engine


class ResultModel(Base):
    __tablename__ = "results"

    id = Column(Integer, primary_key=True, index=True)
    patient_id = Column(Integer, index=True)
    test_name = Column(String, index=True)
    result_value = Column(Float)
    unit = Column(String)
    result_date = Column(DateTime)
    lab_name = Column(String)


# Create the database tables
Base.metadata.create_all(bind=engine)
