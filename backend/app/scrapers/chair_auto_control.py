import logging
import re
from .run_crawl4ai import run_crawl4ai

logger = logging.getLogger(__name__)


def parse_chair_auto_thesis_list(markdown_text: str) -> list[dict]:
    """
    From the given markdown, extract bullet lines that specifically start with
    either:
      * Thesis / Project:
    or
      * Thesis:

    Then capture the bracketed title [Title] and the link (URL) from:
      (URL "Tooltip")
    ignoring any optional tooltip part.

    Returns a list of dicts: [{ 'title': ..., 'link': ... }, ...].
    """

    results = []
    lines = markdown_text.splitlines()

    # Regex explanation:
    #   ^\s*\*\s+ => bullet line, e.g. "* " plus optional spaces
    #   (?:Thesis\s*/\s*Project|Thesis): => matches "Thesis / Project:" or "Thesis:"
    #   \s+ => one or more spaces
    #   \[(.*?)\] => bracketed text (title)
    #   \(([^)]+)\) => parenthesized link part
    #
    # Example line matched:
    #   * Thesis / Project: [Controller Synthesis ...](https://www.ac.tf.fau.eu/... "foo")

    pattern = re.compile(
        r'^\s*\*\s+(?:Thesis\s*/\s*Project|Thesis):\s+\[(.*?)\]\(([^)]+)\)'
    )

    for line in lines:
        stripped = line.strip()
        match = pattern.match(stripped)
        if match:
            title = match.group(1).strip()
            link_part = match.group(2).strip()

            # If there's a tooltip in quotes after the URL, remove it.
            # e.g.:  https://www.ac.tf.fau.eu/...pdf "Background: ..."
            tooltip_pattern = re.compile(r'^([^"]+)(?:\s+"[^"]*")?$')
            link_match = tooltip_pattern.match(link_part)
            if link_match:
                actual_url = link_match.group(1).strip()
            else:
                actual_url = link_part

            results.append({"title": title, "link": actual_url})

    return results


async def scrape_chair_auto_control(url: str) -> list[dict]:
    """
    Scrape the Chair of Automatic Control page using crawl4ai,
    returning a list of bullet items from "##  Explicit thesis topics".
    We ignore anything after "##  Research areas".

    """
    logger.info(f"Scraping Chair of Automatic Control => {url}")
    try:
        result = await run_crawl4ai(url, verbose=False)
        markdown_text = result.markdown
        logger.debug(
            f"Chair Auto Control markdown length: {len(markdown_text)}")

        thesis_list = parse_chair_auto_thesis_list(markdown_text)
        logger.info(
            f"Chair of Automatic Control => extracted {len(thesis_list)} items.")
        return thesis_list

    except Exception as exc:
        logger.exception(f"Error scraping Chair of Automatic Control: {exc}")
        return []
