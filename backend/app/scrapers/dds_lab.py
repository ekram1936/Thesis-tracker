import logging
import re
from .run_crawl4ai import run_crawl4ai

logger = logging.getLogger(__name__)


def parse_dds_thesis_list(markdown_text: str) -> list[dict]:
    """
    Parse the markdown from DDS Lab to extract master's thesis entries from:
      ## Topic proposals (with corresponding advisers)
    ...up to the next '## ' heading.

    Each item is returned as {'title': ..., 'link': ...}.
    """
    results = []

    # 1. Split the markdown into sections by headings (## ...)
    sections = re.split(r'##\s+', markdown_text)

    # 2. Find the "Topic proposals" section
    topic_section = None
    for section in sections:
        if section.lower().startswith("topic proposals"):
            topic_section = section
            break

    if topic_section is None:
        logger.warning("No 'Topic proposals' section found.")
        return results

    # 3. Extract bullet points from the "Topic proposals" section
    thesis_pattern = re.compile(r'\*\s+\[(.*?)\]\((https?://[^\s)]+)\)')

    for line in topic_section.splitlines():
        stripped = line.strip()

        match = thesis_pattern.match(stripped)
        if match:
            title = match.group(1).strip()
            link = match.group(2).strip()

            results.append({
                "title": title,
                "link": link
            })

    return results


async def scrape_dds_lab(url: str) -> list[dict]:
    """
    Scrape the DDS Lab page using crawl4ai, returning
    a list of master's thesis entries.
    """
    logger.info(f"Scraping DDS Lab => {url}")

    try:
        result = await run_crawl4ai(url, verbose=False)
        markdown_text = result.markdown
        logger.debug(f"DDS Lab markdown length: {len(markdown_text)}")
        thesis_list = parse_dds_thesis_list(markdown_text)
        logger.info(
            f"DDS Lab => extracted {len(thesis_list)} master's thesis items."
        )

        return thesis_list

    except Exception as exc:
        logger.exception(f"Error scraping DDS Lab: {exc}")
        return []
