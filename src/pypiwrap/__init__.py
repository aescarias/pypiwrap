"""pypiwrap is an API wrapper for the Python Package Index."""

from ._version import __author__, __license__, __name__, __version__
from .client import PyPIClient, SimpleRepoClient

__all__ = (
    "SimpleRepoClient",
    "PyPIClient",
    "__name__",
    "__author__",
    "__version__",
    "__license__",
)
