from fastapi import APIRouter, HTTPException, Depends
from sqlalchemy.orm import Session
from ...database.database import get_db
from ...database.models import init_db
from ...database.schemas import LabCreate
from ...database.crud import lab_exists, add_new_lab
import logging

logger = logging.getLogger(__name__)

router = APIRouter()


@router.post("/insert_lab")
def insert_lab(labs: list[LabCreate], db: Session = Depends(get_db)):
    """
    Insert a list of labs into the database, ensuring no duplicates.
    Initializes the database if necessary.

    Args:
        labs (list[LabCreate]): List of labs to insert.
        db (Session): Database session dependency.

    Returns:
        dict: Summary of inserted and skipped labs.
    """
    try:
        # Initialize the database to ensure tables exist
        init_db()
        logger.info("Database initialized successfully.")

        inserted_count = 0
        skipped_count = 0

        for lab_data in labs:
            try:
                # Check if the lab exists
                if lab_exists(db, lab_data.lab_name, str(lab_data.lab_url)):
                    logger.info(f"Skipped existing lab: {lab_data.lab_name}")
                    skipped_count += 1
                    continue

                # Add the new lab
                add_new_lab(db, lab_data)
                inserted_count += 1
                logger.info(f"Inserted new lab: {lab_data.lab_name}")

            except Exception as e:
                logger.error(
                    f"Error processing lab: {lab_data.lab_name}. Error: {e}")
                continue

        logger.info(
            f"Insert operation completed: {inserted_count} labs inserted, {skipped_count} labs skipped."
        )
        return {"status": "success", "inserted": inserted_count, "skipped": skipped_count}

    except Exception as e:
        logger.exception("Error inserting labs.")
        raise HTTPException(status_code=500, detail="Failed to insert labs.")
