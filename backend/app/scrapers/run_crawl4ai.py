from crawl4ai import AsyncWebCrawler, BrowserConfig, CacheMode
import asyncio
from crawl4ai import AsyncWebCrawler, CacheMode
from playwright.sync_api import sync_playwright


async def run_crawl4ai(url: str, verbose: bool = False):
    """
    The single function that runs crawl4ai for a given URL.
    Returns the entire 'result' object from which you can parse:
      - result.markdown_v2.raw_markdown
      - result.html_v2
      - etc.
    """
    async with AsyncWebCrawler(verbose=verbose) as crawler:
        result = await crawler.arun(url=url, cach_mode=CacheMode.ENABLED)
    return result


def crawl_url(url: str, verbose: bool = False):
    """A sync wrapper, if needed outside async context."""
    return asyncio.run(run_crawl4ai(url, verbose=verbose))


# with sync_playwright() as p:
#     # Channel can be "chrome", "msedge", "chrome-beta", "msedge-beta" or "msedge-dev".
#     browser = p.chromium.launch(channel="msedge")
#     page = browser.new_page()
#     page.goto("http://playwright.dev")
#     print(page.title())
#     browser.close()


# async def run_crawl4ai(url: str, verbose: bool = True):
#     """
#     The single function that runs crawl4ai for a given URL.
#     Returns the entire 'result' object from which you can parse:
#       - result.markdown_v2.raw_markdown
#     """
#     sync_playwright()
#     # Recommended way: Initialize BrowserConfig with desired settings
#     browser_config = BrowserConfig(
#         browser_type="chromium", headless=True, verbose=verbose)

#     # Use AsyncWebCrawler with the BrowserConfig
#     async with AsyncWebCrawler(config=browser_config) as crawler:
#         # Perform the crawling operation
#         result = await crawler.arun(url=url, cache_mode=CacheMode.ENABLED)
#     return result


# def crawl_url(url: str, verbose: bool = True):
#     """
#     A synchronous wrapper for the asynchronous function, useful outside async contexts.
#     """
#     return asyncio.run(run_crawl4ai(url, verbose=verbose))


# import asyncio
# from playwright.async_api import async_playwright
# from crawl4ai import AsyncWebCrawler, BrowserConfig, CacheMode


# async def run_crawl4ai(url: str, verbose: bool = True):
#     """
#     The single function that runs crawl4ai for a given URL.
#     Returns the entire 'result' object from which you can parse:
#       - result.markdown_v2.raw_markdown
#     """
#     # Use async_playwright
#     async with async_playwright() as p:
#         # Launch browser (channel can be "msedge", "chrome", etc.)
#         browser = await p.chromium.launch(channel='chromium', headless=True)
#         page = await browser.new_page()
#         await page.goto(url)
#         page_title = await page.title()
#         print(f"Page Title: {page_title}")

#         # Close the browser after use
#         await browser.close()

#     # Recommended way: Initialize BrowserConfig with desired settings
#     browser_config = BrowserConfig(
#         browser_type="chromium", headless=True, verbose=verbose
#     )

#     # Use AsyncWebCrawler with the BrowserConfig
#     async with AsyncWebCrawler(config=browser_config) as crawler:
#         # Perform the crawling operation
#         result = await crawler.arun(url=url, cache_mode=CacheMode.ENABLED)
#     return result


# def crawl_url(url: str, verbose: bool = True):
#     """
#     A synchronous wrapper for the asynchronous function, useful outside async contexts.
#     """
#     return asyncio.run(run_crawl4ai(url, verbose=verbose))
