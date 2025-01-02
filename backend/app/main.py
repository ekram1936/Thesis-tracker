from datetime import datetime
import logging
import sys
import os
from fastapi import FastAPI
from logging.handlers import RotatingFileHandler

from .routers.scrape import router as scrape_router
from .routers.insert_thesis_topic import router as insert_thesis_topic_router
from .routers.insert_lab import router as insert_lab_router
from .routers.insights import router as insights_router
from .routers.thesis_topics_with_lab import router as thesis_topics_with_lab_router


def configure_logging():
    """
    Configures logging to log messages to both the console and a rotating log file.
    """

    log_dir = os.getenv("LOG_DIR", "logs")

    if not os.path.exists(log_dir):
        os.makedirs(log_dir)
        print(f"Log directory created: {log_dir}")

    log_file = os.path.join(
        log_dir, f"MTA_{datetime.now().strftime('%Y%m%d_%H%M%S')}.log")

    logger = logging.getLogger()
    logger.setLevel(logging.INFO)

    # Formatter for log messages
    log_format = "%(asctime)s [%(levelname)s] %(name)s: %(message)s"
    formatter = logging.Formatter(log_format)

    console_handler = logging.StreamHandler(sys.stdout)
    console_handler.setLevel(logging.INFO)
    console_handler.setFormatter(formatter)
    logger.addHandler(console_handler)

    # Rotating file handler
    rotating_file_handler = RotatingFileHandler(
        log_file,
        maxBytes=5 * 1024 * 1024,
        backupCount=5,
    )
    rotating_file_handler.setLevel(logging.INFO)
    rotating_file_handler.setFormatter(formatter)
    logger.addHandler(rotating_file_handler)
    logger.info(f"Logging initialized. Logs are being written to {log_file}")


def create_app():
    configure_logging()

    app = FastAPI(title="Master Thesis Topics from Different Labs",)

    app.include_router(scrape_router, prefix="/api", tags=["scrape"])
    app.include_router(insert_thesis_topic_router,
                       prefix="/api", tags=["insert_thesis_topic"])
    app.include_router(insert_lab_router, prefix="/api", tags=["insert_lab"])
    app.include_router(insights_router, prefix="/api", tags=["insights"])
    app.include_router(
        thesis_topics_with_lab_router, prefix="/api", tags=["thesis_topics_with_lab"])

    @app.get("/")
    def root():
        return {"message": "Welcome to Master Thesis Topics from Different Labs"}

    return app


app = create_app()
