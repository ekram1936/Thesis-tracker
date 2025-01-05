from sqlalchemy import func
from sqlalchemy.orm import Session
from sqlalchemy.exc import SQLAlchemyError
from .models import Lab, ThesisTopic, TopicStatus
from .schemas import LabCreate, ThesisTopicCreate
import logging
from datetime import datetime


logger = logging.getLogger(__name__)


def get_lab_id_mapping(session: Session):
    """
    Fetch all labs and return a mapping of lab_name to lab_id.
    Args:
        session (Session): SQLAlchemy database session.

    Returns:
        dict: Mapping of lab_name to lab_id.
    """
    try:
        labs = session.query(Lab).all()
        return {lab.lab_name: lab.lab_id for lab in labs}
    except SQLAlchemyError as e:
        logger.exception("Error fetching lab ID mapping.")
        raise


def get_lab_by_name(session: Session, lab_name: str):
    """
    Retrieve a lab by its name.
    """
    try:
        return session.query(Lab).filter_by(lab_name=lab_name).first()
    except SQLAlchemyError as e:
        logger.exception("Error querying lab by name.")
        raise


def lab_exists(session: Session, lab_name: str, lab_url: str):
    """
    Check if a lab exists based on its name and URL.
    """
    try:
        return session.query(Lab).filter_by(lab_name=lab_name, lab_url=lab_url).first()
    except SQLAlchemyError as e:
        logger.exception("Error checking if lab exists.")
        raise


def add_new_lab(session: Session, lab_data: LabCreate):
    """
    Add a new lab to the database.
    """
    try:
        lab = Lab(lab_name=lab_data.lab_name, lab_url=lab_data.lab_url)
        session.add(lab)
        session.commit()
        session.refresh(lab)
        logger.info(f"Lab added: {lab.lab_name}")
        return lab
    except SQLAlchemyError as e:
        session.rollback()
        logger.exception("Failed to add lab.")
        raise

# CRUD for thesis topics


def get_all_topics(session: Session):
    """
    Retrieve all thesis topics from the database.
    """
    try:
        return session.query(ThesisTopic).all()
    except SQLAlchemyError as e:
        logger.exception("Error querying all thesis topics.")
        raise


def get_topic_by_key(session: Session, title: str, lab_id: int):
    """
    Retrieve a specific thesis topic by its title and lab ID.
    """
    try:
        return session.query(ThesisTopic).filter_by(mt_title=title, lab_id=lab_id).first()
    except SQLAlchemyError as e:
        logger.exception("Error querying topic by title and lab ID.")
        raise


def add_new_thesis_topic(session: Session, title: str, url: str, lab_id: int):
    """
    Add a new thesis topic to the database.
    """
    try:
        topic = ThesisTopic(
            mt_title=title,
            mt_url=url,
            lab_id=lab_id,
            added_date=datetime.now(),
            status=TopicStatus.OPEN,
        )
        session.add(topic)
        session.commit()
        session.refresh(topic)
        logger.info(f"Thesis topic added: {title}")
        return topic
    except SQLAlchemyError as e:
        session.rollback()
        logger.exception("Failed to add thesis topic.")
        raise


def update_topic_status(session: Session, topic: ThesisTopic, new_status: TopicStatus):
    """
    Update the status of an existing topic.

    Args:
        session (Session): Database session.
        topic (ThesisTopic): The topic object to update.
        new_status (TopicStatus): The new status to set.
    """
    try:
        topic.status = new_status
        session.commit()
        logger.info(
            f"Updated topic status to {new_status} for topic: {topic.mt_title}")
    except SQLAlchemyError as e:
        session.rollback()
        logger.exception("Failed to update topic status.")
        raise


def get_total_labs(session: Session) -> int:
    """
    Get the total number of labs.
    """
    try:
        return session.query(Lab).count()
    except SQLAlchemyError as e:
        logger.exception("Error fetching total number of labs.")
        raise


def get_total_open_thesis(session: Session) -> int:
    """
    Get the total number of open thesis topics.
    """
    try:
        return session.query(ThesisTopic).filter_by(status=TopicStatus.OPEN).count()
    except SQLAlchemyError as e:
        logger.exception("Error fetching total number of open thesis topics.")
        raise


def get_total_closed_thesis(session: Session) -> int:
    """
    Get the total number of closed thesis topics.
    """
    try:
        return session.query(ThesisTopic).filter_by(status=TopicStatus.CLOSED).count()
    except SQLAlchemyError as e:
        logger.exception(
            "Error fetching total number of closed thesis topics.")
        raise


def get_thesis_per_lab(session: Session) -> dict:
    """
    Get the number of thesis topics per lab.

    Returns:
        dict: A mapping of lab names to the count of thesis topics in each lab.
    """
    try:
        results = (
            session.query(Lab.lab_name, func.count(ThesisTopic.topic_id))
            .join(ThesisTopic, Lab.lab_id == ThesisTopic.lab_id)
            .group_by(Lab.lab_name)
            .all()
        )
        return {lab_name: count for lab_name, count in results}
    except SQLAlchemyError as e:
        logger.exception("Error fetching thesis topics per lab.")
        raise


def get_labs_with_topics(session: Session):
    labs = session.query(Lab).all()
    result = []
    for lab in labs:
        topics = session.query(ThesisTopic).filter(
            ThesisTopic.lab_id == lab.lab_id).all()
        result.append({
            "lab_name": lab.lab_name,
            "lab_url": lab.lab_url,
            "topics": [
                {
                    "title": topic.mt_title,
                    "status": topic.status,
                    "url": topic.mt_url  # Ensure this field is added
                }
                for topic in topics
            ]
        })
    return result
