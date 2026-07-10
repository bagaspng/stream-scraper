"""
Custom exceptions for the stream scraper package.
"""


class StreamNotFoundError(Exception):
    """Base exception for any failure to locate stream information."""
    pass


class UUIDNotFoundError(StreamNotFoundError):
    """Raised when the uuid value cannot be located in the page."""
    pass


class ServerNotFoundError(StreamNotFoundError):
    """Raised when the server value cannot be located in the page."""
    pass
