import logging
import re
from urllib.parse import urljoin
from .run_crawl4ai import run_crawl4ai

logger = logging.getLogger(__name__)


def parse_madlab_thesis_list(markdown_text: str, base_url: str) -> list[dict]:
    """
    Parse the provided `markdown_text` to extract a list of MAD LabMaster's Thesis entries.
    Each entry is returned as a dictionary with keys: 'title', 'link'.
    Ensures the link is absolute by joining it with `base_url`.
    """
    results = []
    try:
        lines = markdown_text.splitlines()
        start_index = None
        for i, line in enumerate(lines):
            if line.strip().lower().startswith("##  master's thesis"):
                start_index = i
                break

        if start_index is None:
            logger.warning(
                "No '##  Master's Thesis' heading found in markdown.")
            return results

        pattern = re.compile(r'^##### \[(.*?)\]\((.*?)\)')

        for line in lines[start_index + 1:]:
            if line.strip().startswith("## "):
                break

            match = pattern.match(line.strip())
            if match:
                title = match.group(1).strip()
                relative_link = match.group(2).strip()
                full_link = urljoin(base_url, relative_link)
                results.append({"title": title, "link": full_link})

    except Exception as e:
        logger.exception(
            f"Error while parsing MAD Lab Master's Thesis List from markdown: {e}")

    return results


async def scrape_mad_lab(url: str) -> list[dict]:
    """
    Scrape the MAD Lab page using crawl4ai, returning a list of 
    dictionaries representing MAD Lab Master's Thesis entries.

    """
    logger.info(f"Scraping MAD Lab => {url}")

    try:
        result = await run_crawl4ai(url, verbose=False)
        markdown_text = result.markdown
        logger.debug(f"Markdown text length: {len(markdown_text)} chars")
        base_url_mad_lab = "https://www.mad.tf.fau.de/"
        mad_thesis_list = parse_madlab_thesis_list(
            markdown_text, base_url_mad_lab)
        logger.info(
            f"MAD Lab => extracted {len(mad_thesis_list)} master's thesis items."
        )

        return mad_thesis_list

    except Exception as exc:
        logger.exception(f"Error scraping MAD Lab: {exc}")
        return []
