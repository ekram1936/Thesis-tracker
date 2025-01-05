from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from ...database.database import get_db
from ...database.crud import get_labs_with_topics

router = APIRouter()


@router.get("/thesis_topics", summary="Get all labs with their thesis topics")
def fetch_labs_with_topics(db: Session = Depends(get_db)):
    """
    Fetch all labs along with their associated thesis topics.

    Args:
        db (Session): Database session dependency.

    Returns:
        list: A list of labs with their thesis topics.
    """
    try:
        labs = get_labs_with_topics(db)
        return labs
    except Exception as e:
        raise HTTPException(
            status_code=500, detail="Failed to fetch labs and topics")
