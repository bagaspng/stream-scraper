"""
Data models used across the scraper package.
"""

from dataclasses import dataclass


@dataclass
class RawStreamData:
    """Raw values pulled straight out of the HTML, before URL construction."""
    uuid: str
    server: str


@dataclass
class StreamInfo:
    """Final, ready-to-export stream information."""
    uuid: str
    server: str
    channel: int
    websocket: str