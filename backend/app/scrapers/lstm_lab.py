import logging
import re
from bs4 import BeautifulSoup

from .run_crawl4ai import run_crawl4ai

logger = logging.getLogger(__name__)


def parse_lstm_thesis_list(markdown_text: str) -> list[dict]:
    """
    Parse the markdown from LSTM Lab to extract master's thesis entries from:
      ##  Advertised Thesis Subjects
    ...up to (but not including) the line:
      **Assigned Subjects**

    Each item is returned as {'title': ..., 'link': ...}.

    Steps:
      1. Locate the '##  Advertised Thesis Subjects' heading.
      2. Collect bullet lines until we see either a new '## ' heading
         OR '**Assigned Subjects**'.
      3. Extract bracketed title and link from lines like:
         * [Some Title](https://some.url "Optional Tooltip")
    """
    results = []
    lines = markdown_text.splitlines()

    # 1. Find the "##  Advertised Thesis Subjects" heading
    start_index = None
    for i, line in enumerate(lines):
        if line.strip().lower().startswith("##  advertised thesis subjects"):
            start_index = i
            break

    if start_index is None:
        logger.warning("No '##  Advertised Thesis Subjects' heading found.")
        return results  # empty list

    # 2. We'll parse lines after that heading. Stop if we see another "## "
    #    OR the line "**Assigned Subjects**".
    bullet_pattern = re.compile(r'^\s*\*\s+\[(.*?)\]\(([^)]+)\)')

    for line in lines[start_index + 1:]:
        stripped = line.strip()
        # Stop conditions
        if stripped.startswith("## "):
            break
        if stripped == "**Assigned Subjects**":
            break

        match = bullet_pattern.match(stripped)
        if match:
            title = match.group(1).strip()
            link_part = match.group(2).strip()
            # If there's a tooltip after the URL, remove it.
            # e.g.:  https://... "Background..."
            m2 = re.match(r'^(https?://[^\s]+)(?:\s+"(.*)")?$', link_part)
            if m2:
                actual_url = m2.group(1)
            else:
                actual_url = link_part  # fallback if pattern changes

            results.append({"title": title, "link": actual_url})

    return results


async def scrape_lstm_lab(url: str) -> list[dict]:
    """
    Scrape the LSTM Lab page using crawl4ai, returning
    a list of master's thesis entries.
    """
    logger.info(f"Scraping LSTM Lab => {url}")

    try:
        # 1. Use crawl4ai to get the markdown
        result = await run_crawl4ai(url, verbose=False)
        markdown_text = result.markdown
        logger.debug(f"LSTM markdown text length: {len(markdown_text)}")

        # 2. Parse the thesis list
        thesis_list = parse_lstm_thesis_list(markdown_text)
        logger.info(
            f"LSTM Lab => extracted {len(thesis_list)} master's thesis items.")

        return thesis_list

    except Exception as exc:
        # If anything else goes wrong (network error, site structure change, etc.)
        # we log the traceback and return an empty list
        logger.exception(f"Error scraping LSTM Lab: {exc}")
        return []
