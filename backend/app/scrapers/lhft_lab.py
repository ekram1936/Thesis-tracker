import logging
import re
from .run_crawl4ai import run_crawl4ai

logger = logging.getLogger(__name__)


def parse_lhft_thesis_list(markdown_text: str) -> list[dict]:
    """
    Parse the markdown to extract only master's thesis topics (MA)
    from the "Abschlussarbeiten" section.
    """
    results = []
    markdown_text = markdown_text.replace('\n', ' ').strip()
    thesis_section = re.search(
        r'##\s*ab[sch]+lussarbeiten.*?(\*\*BA:.*?)(?=##|\Z)', markdown_text, re.DOTALL | re.IGNORECASE)
    if not thesis_section:
        print("No 'Abschlussarbeiten' section found.")
        return results

    section_text = thesis_section.group(1)
    logger.debug(f"Extracted Abschlussarbeiten section:\n{section_text}")

    thesis_pattern = re.compile(
        r'\*\s+\[(.*?MA.*?)\]\((https?://[^\s)]+)\)', re.DOTALL)
    for match in thesis_pattern.finditer(section_text):
        title = match.group(1).strip()
        link = match.group(2).strip()

        results.append({
            "title": title,
            "link": link
        })

    return results


async def scrape_lhft_lab(url: str) -> list[dict]:
    """
    Scrape the LHFT Lab page using crawl4ai, returning
    a list of master's thesis entries containing "MA".
    """
    logger.info(f"Scraping LHFT Lab => {url}")

    try:
        result = await run_crawl4ai(url, verbose=False)
        html_text = result.markdown  # Use markdown instead of raw HTML
        logger.debug(f"LHFT Lab Markdown length: {len(html_text)}")

        thesis_list = parse_lhft_thesis_list(html_text)
        logger.info(
            f"LHFT Lab => extracted {len(thesis_list)} master's thesis items."
        )

        return thesis_list

    except Exception as exc:
        logger.exception(f"Error scraping LHFT Lab: {exc}")
        return []
