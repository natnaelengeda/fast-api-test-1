from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, declarative_base
from dotenv import load_dotenv
import os

# Load .env variables
load_dotenv()

# Environment variables
DATABASE_USERNAME = os.getenv("DATABASE_USERNAME")
DATABASE_PASSWORD = os.getenv("DATABASE_PASSWORD")
DATABASE_HOST     = os.getenv("DATABASE_HOST")
DATABASE_PORT     = os.getenv("DATABASE_PORT", "5432")
DATABASE_NAME     = os.getenv("DATABASE_NAME")

# Build connection string
DATABASE_URL = f"postgresql://{DATABASE_USERNAME}:{DATABASE_PASSWORD}@{DATABASE_HOST}:{DATABASE_PORT}/{DATABASE_NAME}"

# Create engine and session
engine = create_engine(DATABASE_URL)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

# Base class for models
Base = declarative_base()

# Dependency to get DB session
def get_session():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()
