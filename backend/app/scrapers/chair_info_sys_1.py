import logging
import re
from .run_crawl4ai import run_crawl4ai

logger = logging.getLogger(__name__)

EXCLUDED_TITLES = {
    "Contact & Address",
    "Jobs",
    "Privacy",
    "Accessibility",
    "Imprint",
    "Facebook",
    "Twitter",
    "RSS Feed"
}


def parse_information_systems_thesis_list(markdown_text: str) -> list[dict]:
    """
    Parse the Chair of Information Systems I markdown to extract the list
    of thesis topics from the '## Master Thesis Offerings' section.

    This function:
      - Starts parsing at the '## Master Thesis Offerings' heading.
      - Skips lines until the first "|" is found (ignoring '---|---').
      - Collects valid bullet points after the delimiter.
      - Stops parsing at the next heading (e.g., '## Bachelor Thesis Offerings' or EOF).
      - Excludes any titles in the EXCLUDED_TITLES set.
    """
    results = []
    try:
        lines = markdown_text.splitlines()
        start_index = None
        for i, line in enumerate(lines):
            if line.strip().lower().startswith("## master thesis offerings"):
                start_index = i
                break

        if start_index is None:
            logger.warning("No '## Master Thesis Offerings' heading found.")
            return results

        delimiter_index = None
        for j in range(start_index + 1, len(lines)):
            line = lines[j].strip()
            if line == "---|---":
                continue
            if "|" in line:
                delimiter_index = j
                break

        if delimiter_index is None:
            logger.warning(
                "No '|' delimiter found in '## Master Thesis Offerings' section.")
            return results

        end_index = None
        for k in range(delimiter_index + 1, len(lines)):
            if lines[k].strip().startswith("## "):
                end_index = k
                break

        if end_index is None:
            end_index = len(lines)

        pattern = re.compile(r'^\*\s+\[(.*?)\]\((.*?)\)$')

        for idx in range(delimiter_index + 1, end_index):
            line = lines[idx].strip()
            match = pattern.match(line)
            if match:
                title = match.group(1).strip()
                link = match.group(2).strip()

                if title in EXCLUDED_TITLES:
                    continue
                results.append({"title": title, "link": link})

    except Exception as e:
        logger.exception(
            f"Error parsing Chair of Information Systems markdown: {e}")

    return results


async def scrape_information_systems(url: str) -> list[dict]:
    """
    Scrape the Chair of Information Systems I page using crawl4ai,
    looking specifically for the '## Master Thesis Offerings' section.

    Returns:
      - List of dictionaries with 'title' and 'link'.
    """
    logger.info(f"Scraping Chair of Information Systems I => {url}")
    try:
        result = await run_crawl4ai(url, verbose=False)
        markdown_text = result.markdown
        logger.debug(f"Markdown length: {len(markdown_text)}")

        thesis_list = parse_information_systems_thesis_list(markdown_text)
        logger.info(
            f"Extracted {len(thesis_list)} items from '## Master Thesis Offerings'.")
        return thesis_list

    except Exception as exc:
        logger.exception(
            f"Error scraping Chair of Information Systems I: {exc}")
        return []
