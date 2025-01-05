from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from ...database.database import get_db
from ...database.crud import (
    get_total_labs,
    get_total_open_thesis,
    get_total_closed_thesis,
    get_thesis_per_lab,
)

router = APIRouter()


@router.get("/insights/total_labs")
def fetch_total_labs(db: Session = Depends(get_db)):
    """
    API endpoint to get the total number of labs.
    """
    try:
        total_labs = get_total_labs(db)
        return total_labs
    except Exception as e:
        raise HTTPException(
            status_code=500, detail="Failed to fetch total labs.")


@router.get("/insights/total_open_thesis")
def fetch_total_open_thesis(db: Session = Depends(get_db)):
    """
    API endpoint to get the total number of open thesis topics.
    """
    try:
        total_open_thesis = get_total_open_thesis(db)
        return total_open_thesis
    except Exception as e:
        raise HTTPException(
            status_code=500, detail="Failed to fetch total open thesis topics."
        )


@router.get("/insights/total_closed_thesis")
def fetch_total_closed_thesis(db: Session = Depends(get_db)):
    """
    API endpoint to get the total number of closed thesis topics.
    """
    try:
        total_closed_thesis = get_total_closed_thesis(db)
        return total_closed_thesis
    except Exception as e:
        raise HTTPException(
            status_code=500, detail="Failed to fetch total closed thesis topics."
        )


@router.get("/insights/thesis_per_lab")
def fetch_thesis_per_lab(db: Session = Depends(get_db)):
    """
    API endpoint to get the number of thesis topics per lab.
    """
    try:
        thesis_per_lab = get_thesis_per_lab(db)
        return thesis_per_lab
    except Exception as e:
        raise HTTPException(
            status_code=500, detail="Failed to fetch thesis topics per lab."
        )
