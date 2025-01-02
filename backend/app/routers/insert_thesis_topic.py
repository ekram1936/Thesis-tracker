import json
from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from database.database import get_db
from database.models import Lab, init_db, TopicStatus
from ..routers.scrape import scrape_all
from ..routers.insert_lab import insert_lab
from database.schemas import LabCreate
from database.crud import get_all_topics, add_new_thesis_topic, get_lab_id_mapping, update_topic_status
import logging

logger = logging.getLogger(__name__)

router = APIRouter()


@router.post("/insert_thesis_topic")
async def sync_thesis_topics(db: Session = Depends(get_db)):
    """
    Synchronize thesis topics:
    - Initialize the database.
    - Scrape data to get labs and thesis topics.
    - Insert new labs.
    - Insert thesis topics for each Lab.
    - Set topics missing from the scraped data to "closed".

    Args:
        db (Session): Database session dependency.

    Returns:
        dict: Summary of inserted, skipped, and closed thesis topics.
    """
    try:
        # Step 1: Initialize the database
        logger.info("Initializing the database.")
        init_db()

        # Step 2: Scrape data
        logger.info("Starting the scraping process.")
        scrape_result = await scrape_all()
        labs = scrape_result["all_labs"]
        topics = scrape_result["all_thesis_topics"]
        # with open("scrape_results_20241228_131101.json", "r", encoding="utf-8") as f:
        #     scrape_result = json.load(f)

        # labs = scrape_result["labs"]
        # topics = scrape_result["thesis_topics"]

        # Step 3: Insert labs
        logger.info("Inserting labs into the database.")
        lab_create_list = [
            LabCreate(lab_name=lab["lab_name"], lab_url=lab["lab_url"])
            for lab in labs
        ]
        insert_lab(lab_create_list, db)

        # Fetch lab IDs for mapping
        lab_id_mapping = lab_id_mapping = get_lab_id_mapping(db)

        # Step 4: Process thesis topics
        logger.info("Processing thesis topics.")
        inserted_count = 0
        skipped_count = 0
        closed_count = 0
        reopened_count = 0

        # Existing topics in the database
        existing_topics = get_all_topics(db)
        existing_topic_map = {
            (t.mt_title, t.lab_id): t for t in existing_topics
        }

        # Scraped topics to compare
        scraped_topic_keys = set()

        for topic in topics:
            lab_id = lab_id_mapping.get(topic["lab_name"])
            if not lab_id:
                logger.warning(
                    f"Lab not found for thesis topic: {topic['thesis_title']}. Skipping."
                )
                continue

            topic_key = (topic["thesis_title"], lab_id)
            scraped_topic_keys.add(topic_key)

            # Check if the topic already exists
            # if topic_key not in existing_topic_map:
            #     add_new_thesis_topic(db, topic["thesis_title"],
            #                          topic["thesis_url"], lab_id)
            #     inserted_count += 1
            # else:
            #     skipped_count += 1
            #     logger.info(
            #         f"Skipped existing thesis topic: {topic['thesis_title']}")
            existing_topic = existing_topic_map.get(topic_key)
            if existing_topic:
                if existing_topic.status == TopicStatus.CLOSED:
                    # Reopen the closed topic
                    update_topic_status(db, existing_topic, TopicStatus.OPEN)
                    reopened_count += 1
                    logger.info(
                        f"Reopened closed thesis topic: {topic['thesis_title']}")
                else:
                    skipped_count += 1
                    logger.info(
                        f"Skipped existing open thesis topic: {topic['thesis_title']}")
            else:
                # Add new topic
                add_new_thesis_topic(db, topic["thesis_title"],
                                     topic["thesis_url"], lab_id)
                inserted_count += 1

        # Step 5: Close topics missing in scraped results
        for topic_key, topic_obj in existing_topic_map.items():
            if topic_key not in scraped_topic_keys and topic_obj.status == TopicStatus.OPEN:
                update_topic_status(db, topic_obj, TopicStatus.CLOSED)
                closed_count += 1
                logger.info(f"Set topic to closed: {topic_obj.mt_title}")

        # Summary
        logger.info(
            f"Sync operation completed: {inserted_count} thesis topics inserted, {skipped_count} thesis topics skipped, {closed_count} thesis topics closed."
        )
        return {
            "status": "success",
            "inserted": inserted_count,
            "skipped": skipped_count,
            "reopened": reopened_count,
            "closed": closed_count
        }

    except Exception as e:
        db.rollback()  # Rollback changes on error
        logger.exception("Error synchronizing thesis topics.")
        raise HTTPException(
            status_code=500, detail="Failed to synchronize thesis topics."
        )
