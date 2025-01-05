from sqlalchemy import create_engine, Column, String, Integer, DateTime, ForeignKey, Enum
from sqlalchemy.orm import relationship, sessionmaker
from sqlalchemy.ext.declarative import declarative_base
from datetime import datetime
from sqlalchemy import inspect
import logging
import os
from dotenv import load_dotenv
from sqlalchemy.exc import SQLAlchemyError
import enum


# Load environment variables
load_dotenv()
logger = logging.getLogger(__name__)


# Dynamically construct the DATABASE_URL
DATABASE_USER = os.getenv("DATABASE_USER")
DATABASE_PASSWORD = os.getenv("DATABASE_PASSWORD")
DATABASE_HOST = os.getenv("DATABASE_HOST")
DATABASE_PORT = os.getenv("DATABASE_PORT")
DATABASE_NAME = os.getenv("DATABASE_NAME")

DATABASE_URL = f"postgresql://{DATABASE_USER}:{DATABASE_PASSWORD}@{DATABASE_HOST}:{DATABASE_PORT}/{DATABASE_NAME}"

if None in [DATABASE_USER, DATABASE_PASSWORD, DATABASE_HOST, DATABASE_PORT, DATABASE_NAME]:
    raise ValueError(
        "Database URL construction failed due to environment variable.")


# SQLAlchemy setup
engine = create_engine(DATABASE_URL)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
Base = declarative_base()


class TopicStatus(enum.Enum):
    OPEN = "open"
    CLOSED = "closed"

# Define the labs table


class Lab(Base):
    __tablename__ = "labs"

    lab_id = Column(Integer, primary_key=True, autoincrement=True)
    lab_name = Column(String, nullable=False, unique=True)
    lab_url = Column(String, nullable=False, unique=True)

    thesis_topics = relationship("ThesisTopic", back_populates="lab")

# Define the mt_thesis_topic table


class ThesisTopic(Base):
    __tablename__ = "mt_thesis_topic"

    topic_id = Column(Integer, primary_key=True, index=True)
    mt_title = Column(String, nullable=False)
    mt_url = Column(String, nullable=False)
    added_date = Column(DateTime, default=datetime.now)
    status = Column(Enum(TopicStatus), default=TopicStatus.OPEN)
    lab_id = Column(Integer, ForeignKey("labs.lab_id"), nullable=False)

    lab = relationship("Lab", back_populates="thesis_topics")

# Create the database tables


def init_db():
    """
    Initialize the database by creating tables if they do not already exist.
    Logs the status of table creation.
    """
    try:
        # Inspect the existing tables
        inspector = inspect(engine)
        existing_tables = inspector.get_table_names()

        if existing_tables:
            logger.info(f"Existing tables: {existing_tables}")
        else:
            logger.info("No existing tables found. Creating tables...")

        # Create tables if they do not exist
        Base.metadata.create_all(bind=engine)

        # Log which tables were created
        for table_name in Base.metadata.tables:
            if table_name not in existing_tables:
                logger.info(f"Table created: {table_name}")
            else:
                logger.info(f"Table already exists: {table_name}")

    except SQLAlchemyError as e:
        logger.exception(f"Error initializing database tables: {e}")
        raise
