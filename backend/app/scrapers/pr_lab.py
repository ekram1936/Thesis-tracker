import logging
from bs4 import BeautifulSoup
from .run_crawl4ai import run_crawl4ai

logger = logging.getLogger(__name__)


async def scrape_pr_lab(url: str) -> list[dict]:
    """
    Scrape the PR Lab page using crawl4ai,
    returning list of dictionary items.
    """
    logger.info(f"Scraping PR Lab => {url}")
    # Run crawl4ai
    result = await run_crawl4ai(url, verbose=False)
    print(result.fit_markdown)

    logger.info(f"MAD Lab => extracted results.")
    return result.fit_markdown
