from __future__ import annotations

from dataclasses import dataclass
from datetime import datetime
from xml.etree.ElementTree import Element


@dataclass
class PyPIFeed:
    """A simplified RSS feed returned by PyPI."""

    title: str
    """The title of this feed."""

    link: str
    """A link to the resource being aggregated."""

    description: str
    """A description or summary of this feed."""

    language: str
    """The language of this feed."""

    items: list[PyPIFeedItem]
    """A list of items aggregated in this feed."""

    @classmethod
    def from_xml(cls, element: Element) -> PyPIFeed:
        return cls(
            title=element.findtext("title", ""),
            link=element.findtext("link", ""),
            description=element.findtext("description", ""),
            language=element.findtext("language", ""),
            items=[
                PyPIFeedItem.from_xml(item) for item in (element.findall("item") or [])
            ],
        )


@dataclass
class PyPIFeedItem:
    """A simplified RSS feed item returned by PyPI."""

    title: str
    """The title or topic of this item."""

    link: str
    """A link to the resource being described."""

    guid: str
    """A globally unique identifier for this resource.
    
    In PyPI's case, this is usually the same as :attr:`PyPIFeedItem.link`.
    """

    published_raw: str
    """If provided, a string representing the datetime this resource was published.
    
    This datetime string usually follows RFC 822.
    """

    description: str
    """A description or summary of this item."""

    author: str
    """The author of this item."""

    @classmethod
    def from_xml(cls, element: Element) -> PyPIFeedItem:
        return cls(
            title=element.findtext("title", ""),
            link=element.findtext("link", ""),
            guid=element.findtext("guid", ""),
            published_raw=element.findtext("pubDate", ""),
            description=element.findtext("description", ""),
            author=element.findtext("author", ""),
        )

    @property
    def published(self) -> datetime | None:
        """If provided, the datetime this resource was published."""

        if self.published_raw:
            return datetime.strptime(self.published_raw, "%a, %d %b %Y %H:%M:%S %Z")
