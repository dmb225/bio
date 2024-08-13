from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, declarative_base
from typing import Generator

SQLALCHEMY_DATABASE_URL = "sqlite:///./bio_lab.db"

engine = create_engine(SQLALCHEMY_DATABASE_URL, connect_args={"check_same_thread": False})

SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

Base = declarative_base()

# Dependency to get the database session
def get_db() -> Generator:
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()
