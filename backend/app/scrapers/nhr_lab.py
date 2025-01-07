import re
import logging
from .run_crawl4ai import run_crawl4ai

logger = logging.getLogger(__name__)


def parse_nhr_thesis_list(markdown_text: str) -> list[dict]:
    """
    Parse the markdown to extract only master's thesis topics (Master Thesis) 
    from the "Open theses" section, including markdown link titles.
    Ensure the thesis title is never null.
    """
    results = []
    markdown_text = markdown_text.replace('\n', ' ').strip()

    # Extract the "Open theses" section
    thesis_section = re.search(
        r'##\s*Open theses.*?(?=##|\Z)', markdown_text, re.DOTALL | re.IGNORECASE)
    if not thesis_section:
        logger.warning("No 'Open theses' section found.")
        return results

    section_text = thesis_section.group(0)
    logger.debug(f"Extracted Open Theses section:\n{section_text}")

    # Regex to handle both plain and markdown link titles
    thesis_pattern = re.compile(
        r'\*\s*(?:Bachelor/Master Thesis|Master Thesis):\s*(?:\[(.*?)\]\((https?://[^\s)]+)\)|([^(\[]+))',
        re.DOTALL | re.IGNORECASE
    )

    for match in thesis_pattern.finditer(section_text):
        # Handle different formats
        title_with_link = match.group(1)
        link = match.group(2)
        title_without_link = match.group(3)

        full_title = title_with_link if title_with_link else (
            title_without_link.strip() if title_without_link else "No Title Available")

        # If no link found, set it to empty
        final_link = link if link else ""

        # Add to results
        results.append({
            "title": f"Master Thesis: {full_title}",
            "link": final_link
        })

    return results


async def scrape_nhr_lab(url: str) -> list[dict]:
    """
    Scrape the NHR Lab page using crawl4ai, returning
    a list of master's thesis entries containing "Master Thesis".
    """
    logger.info(f"Scraping NHR Lab => {url}")

    try:
        result = await run_crawl4ai(url, verbose=False)
        markdown_text = result.markdown
        logger.debug(f"NHR Lab Markdown length: {len(markdown_text)}")

        thesis_list = parse_nhr_thesis_list(markdown_text)
        logger.info(
            f"NHR Lab => extracted {len(thesis_list)} master's thesis items.")

        return thesis_list

    except Exception as exc:
        logger.exception(f"Error scraping NHR Lab: {exc}")
        return []
