import re
import logging
from .run_crawl4ai import run_crawl4ai

logger = logging.getLogger(__name__)


def parse_like_thesis_list(markdown_text: str, base_url: str) -> list[dict]:
    """
    Parse the markdown to extract thesis topics from the "Masterarbeiten" section.
    Dynamically generate links based on the sequential collapse index.
    """
    results = []
    markdown_text = markdown_text.replace('\n', ' ').strip()

    # Extract everything after `# Masterarbeiten`
    masterarbeiten_start = re.search(
        r'#\s*Masterarbeiten', markdown_text, re.IGNORECASE)
    if not masterarbeiten_start:
        logger.warning("No 'Masterarbeiten' section found.")
        print("No 'Masterarbeiten' section found.")
        return results

    start_index = masterarbeiten_start.end()
    markdown_after_masterarbeiten = markdown_text[start_index:].strip()

    # Extract all `##` headings until the next top-level heading `#`
    thesis_pattern = re.compile(r'##\s*(.+?)\s*\(ID:\s*(\d+)\)', re.IGNORECASE)
    topics = thesis_pattern.findall(markdown_after_masterarbeiten)

    # Debugging print to see extracted topics
    print(f"Extracted topics: {topics}")

    # Generate links dynamically
    for idx, (title, thesis_id) in enumerate(topics):
        if not title:  # Skip null or empty titles
            continue
        link = f"{base_url}#collapse_{idx}"
        thesis_entry = {
            "title": f"{title.strip()} (ID: {thesis_id.strip()})",
            "link": link
        }
        # Print each entry before appending
        print(f"Adding thesis entry: {thesis_entry}")
        results.append(thesis_entry)

    if not results:
        print("No Master's thesis topics found. Please check the section format.")
    else:
        print(f"Extracted {len(results)} Master's thesis topics.")
    print("Result of LIKE", results)
    return results


async def scrape_like_lab(url: str) -> list[dict]:
    """
    Scrape the LIKE Lab page using crawl4ai, returning
    a list of master's thesis entries containing dynamically generated links.
    """
    logger.info(f"Scraping LIKE Lab => {url}")

    try:
        result = await run_crawl4ai(url, verbose=False)
        markdown_text = result.markdown
        logger.debug(f"LIKE Lab Markdown length: {len(markdown_text)}")

        base_url = "https://www.like.tf.fau.de/lehre/abschlussarbeiten/masterarbeiten/"
        thesis_list = parse_like_thesis_list(markdown_text, base_url)
        logger.info(
            f"LIKE Lab => extracted {len(thesis_list)} master's thesis items.")

        # Final print to see returned list
        print(f"Final list of thesis topics: {thesis_list}")

        return thesis_list

    except Exception as exc:
        logger.exception(f"Error scraping LIKE Lab: {exc}")
        return []
