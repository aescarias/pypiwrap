"""pypiwrap is an API wrapper for the Python Package Index."""

from .client import PyPIClient, PyPIFeedClient, SimpleRepoClient
from .consts import __author__, __license__, __name__, __version__

__all__ = (
    "SimpleRepoClient",
    "PyPIClient",
    "PyPIFeedClient",
    "__name__",
    "__author__",
    "__version__",
    "__license__",
)
