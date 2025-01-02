from fastapi import APIRouter
import requests
import logging
import json
import os
from datetime import datetime

from ..config import LAB_LINKS
from ..scrapers.registry import get_scraper_func

router = APIRouter()
logger = logging.getLogger(__name__)


def validate_link(url: str) -> bool:
    """
    Quick HEAD request to see if link is valid (status < 400).
    Logs warnings if invalid.
    """
    try:
        resp = requests.head(url, timeout=5)
        if resp.status_code < 400:
            logger.info(f"Link is valid: {url}")
            return True
        else:
            logger.warning(f"Link returned status {resp.status_code}: {url}")
            return False
    except Exception as exc:
        logger.warning(f"HEAD request failed for {url}: {exc}")
        return False


@router.post("/scrape")
async def scrape_all():
    """
    POST /api/scrape -> Attempt to scrape each lab from config.json,
    skipping invalid links or unregistered labs. Return summary + data.

    Additionally:
      - Collect lab info in all_labs.
      - Collect thesis topics in all_thesis_topics.
      - Write the results to a JSON file on disk.
    """
    summary = []
    all_labs = []
    all_thesis_topics = []
    results_by_lab = {}  # Store each lab's data here

    for lab_name, url in LAB_LINKS.items():
        logger.info(f"Processing lab '{lab_name}' => {url}")

        # Validate link
        if not validate_link(url):
            msg = f"Skipping lab '{lab_name}', invalid link: {url}"
            logger.warning(msg)
            summary.append(msg)
            continue

        # Retrieve function from registry
        scraper_func = get_scraper_func(lab_name)
        if not scraper_func:
            msg = f"No registered function for '{lab_name}', skipping."
            logger.warning(msg)
            summary.append(msg)
            continue

        # Attempt to scrape
        try:
            logger.info(f"Running scraper for '{lab_name}'...")
            data = await scraper_func(url)
            logger.info(
                f"Scraper for '{lab_name}' succeeded, got {len(data)} items."
            )
            summary.append(f"{lab_name}: extracted {len(data)} items.")

            # Add lab info to all_labs
            all_labs.append({"lab_name": lab_name, "lab_url": url})

            # Add thesis topics to all_thesis_topics
            for item in data:
                all_thesis_topics.append({
                    "lab_name": lab_name,
                    "lab_url": url,
                    "thesis_title": item.get("title"),
                    "thesis_url": item.get("link")
                })

            # Put this lab's data into our dictionary
            results_by_lab[lab_name] = data

        except Exception as e:
            logger.exception(f"Error scraping '{lab_name}': {e}")
            summary.append(f"Error scraping {lab_name}")

    # ---- After scraping all labs, write the results to a JSON file ----
    output_folder = "scrape_results"
    os.makedirs(output_folder, exist_ok=True)
    filename = os.path.join(
        output_folder, f"scrape_results_{datetime.now().strftime('%Y%m%d_%H%M%S')}.json")

    try:
        with open(filename, "w", encoding="utf-8") as f:
            json.dump({"labs": all_labs, "thesis_topics": all_thesis_topics},
                      f, indent=2, ensure_ascii=False)
        logger.info(f"Saved scrape results to {filename}")
    except Exception as file_exc:
        logger.exception(
            f"Failed to write scrape results to {filename}: {file_exc}")
        summary.append(f"Failed to write JSON file: {file_exc}")

    return {"summary": summary, "all_labs": all_labs, "all_thesis_topics": all_thesis_topics}
