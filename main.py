"""
Entry point.

Flow:
    download_html -> parse_stream_info -> save_json

No regex, no BeautifulSoup, no parsing logic here.
All logic lives in the scraper package.
"""

from dataclasses import asdict

import config
from scraper.exceptions import StreamNotFoundError
from scraper.parser import parse_stream_info
from scraper.utils import download_html, save_json, logger


def run(target_url: str = config.TARGET_URL, channel: int = config.CHANNEL) -> None:
    html = download_html(target_url, timeout=config.TIMEOUT)
    stream_info = parse_stream_info(html, channel=channel)

    output = {"stream": asdict(stream_info)}
    save_json(output, config.OUTPUT_FILE)

    logger.info(f"Stream discovered: {output}")


if __name__ == "__main__":
    try:
        run()
    except StreamNotFoundError as exc:
        logger.error(f"Discovery failed: {exc}")