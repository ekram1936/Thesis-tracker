from .models import SessionLocal


def get_db():
    """
    Dependency for managing database sessions.
    """
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()
