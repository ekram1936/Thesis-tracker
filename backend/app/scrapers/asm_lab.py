import logging
import re
from urllib.parse import urljoin
from .run_crawl4ai import run_crawl4ai

logger = logging.getLogger(__name__)


def parse_asm_thesis_list(markdown_text: str, base_url: str) -> list[dict]:
    """
    Parses the ASM markdown to extract Master thesis entries under the 
    heading '##  Masterarbeiten'.

    Each thesis line looks like:
        ## [Title]( /relative/link/ )

    We'll stop if we encounter a new heading like '##  Bachelorarbeiten'
    or any other major heading that indicates we've left the Masterarbeiten section.
    """

    results = []
    try:
        lines = markdown_text.splitlines()

        # 1. Find "##  Masterarbeiten"
        start_index = None
        for i, line in enumerate(lines):
            if line.strip().lower().startswith("##  masterarbeiten"):
                start_index = i
                break

        if start_index is None:
            logger.warning(
                "No '##  Masterarbeiten' heading found in ASM markdown.")
            return results  # empty list if not found

        # 2. We'll parse from start_index+1 onward.
        #    Each thesis is in a line matching:  ## [Title](link)
        #    If we see "##  Bachelorarbeiten" or another major heading, we stop.
        pattern = re.compile(r'^## \[(.*?)\]\((.*?)\)')

        for line in lines[start_index + 1:]:
            stripped = line.strip()

            # If this line is "##  Bachelorarbeiten" or any new heading starting with '## ' (besides our pattern),
            # it means we've left the Masterarbeiten section.
            # We'll do a quick check: if it matches the same pattern we want, we parse it;
            # otherwise we treat it as a new heading to stop parsing.
            if stripped.lower().startswith("##  bachelorarbeiten"):
                break

            # If line starts with "## " but doesn't match our pattern, it's probably a new section => stop.
            if stripped.startswith("## "):
                # see if it matches exactly our "## [Title](...)" pattern
                # (some lines do that for each item, so let's test that first)
                match = pattern.match(stripped)
                if not match:
                    # This means it's a new heading, not a thesis line
                    break
            else:
                # If the line doesn't start with "## " at all, we can skip it
                # or see if there's some unusual formatting. Typically, each thesis is a single line though.
                continue

            # 3. Now parse the thesis line
            match = pattern.match(stripped)
            if match:
                title = match.group(1).strip()
                rel_link = match.group(2).strip()
                # Build absolute link
                full_link = urljoin(base_url, rel_link)

                results.append({"title": title, "link": full_link})

    except Exception as e:
        logger.exception(f"Error parsing ASM Lab markdown: {e}")

    return results


async def scrape_asm_lab(url: str) -> list[dict]:
    """
    Scrape the ASM Lab page using crawl4ai,
    returning a list of master thesis items from 
    the '##  Masterarbeiten' section.
    """
    logger.info(f"Scraping ASM Lab => {url}")
    try:
        # 1. Use crawl4ai to fetch the markdown
        result = await run_crawl4ai(url, verbose=False)
        markdown_text = result.markdown
        logger.debug(f"ASM markdown length: {len(markdown_text)}")

        # 2. Hardcode base domain so relative links become absolute
        base_url_asm = "https://www.asm.tf.fau.de/"

        # 3. Parse the lines
        thesis_list = parse_asm_thesis_list(markdown_text, base_url_asm)
        logger.info(
            f"ASM Lab => extracted {len(thesis_list)} items from Masterarbeiten.")
        return thesis_list

    except Exception as exc:
        logger.exception(f"Error scraping ASM Lab: {exc}")
        return []
