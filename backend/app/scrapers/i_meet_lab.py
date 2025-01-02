import logging
import re
from urllib.parse import urljoin
from .run_crawl4ai import run_crawl4ai

logger = logging.getLogger(__name__)


def parse_i_meet_thesis_list(markdown_text: str, base_url: str) -> list[dict]:
    """
    Revised parser for i-MEET:
      1) Find '# MSc Theses'.
      2) From there, parse lines until we reach:
         '### Research group of Prof. Wellmann (CGL (Crystal Growth Lab))'
      3) For each line in this range, if it matches:
         [TitleInBrackets](RelativeLink)OptionalText
         we capture the bracketed text as 'title' and the link as 'link'.
    """

    results = []
    try:
        lines = markdown_text.splitlines()

        # 1. Find where '# MSc Theses' appears
        start_index = None
        for i, line in enumerate(lines):
            if line.strip().lower().startswith("# msc theses"):
                start_index = i
                break

        if start_index is None:
            logger.warning(
                "No '# MSc Theses' heading found in i-MEET markdown.")
            return results  # empty list

        # 2. We'll parse lines from start_index+1 onward
        #    until we see '### Research group of Prof. Wellmann (CGL (Crystal Growth Lab))'
        end_index = None
        for j in range(start_index + 1, len(lines)):
            if lines[j].strip().startswith("### Research group of Prof. Wellmann (CGL (Crystal Growth Lab))"):
                end_index = j
                break

        # If we never find that line, we parse until the end of the file
        if end_index is None:
            end_index = len(lines)

        # 3. The regex for lines like: [Title](Link)whatever
        pattern = re.compile(r'^\[(.*?)\]\((.*?)\)(.*)$')

        # Loop through the relevant lines
        for idx in range(start_index + 1, end_index):
            text = lines[idx].strip()
            match = pattern.match(text)
            if match:
                bracket_title = match.group(1).strip()
                relative_link = match.group(2).strip()
                # Convert to absolute link
                absolute_link = urljoin(base_url, relative_link)

                results.append({
                    "title": bracket_title,
                    "link": absolute_link
                })

    except Exception as e:
        logger.exception(f"Error parsing i-MEET markdown: {e}")

    return results


async def scrape_i_meet(url: str) -> list[dict]:
    """
    Scrape the i-MEET page using crawl4ai,
    collecting lines from '# MSc Theses' until
    '### Research group of Prof. Wellmann (CGL (Crystal Growth Lab))'
    that match [Title](Link).
    """
    logger.info(f"Scraping i-MEET => {url}")
    try:
        # Fetch markdown via crawl4ai
        result = await run_crawl4ai(url, verbose=False)
        markdown_text = result.markdown
        logger.debug(f"i-MEET markdown length: {len(markdown_text)}")

        base_url = "https://www.i-meet.ww.uni-erlangen.de/"
        thesis_list = parse_i_meet_thesis_list(markdown_text, base_url)
        logger.info(
            f"i-MEET => extracted {len(thesis_list)} items (link pattern only).")
        return thesis_list

    except Exception as exc:
        logger.exception(f"Error scraping i-MEET: {exc}")
        return []
