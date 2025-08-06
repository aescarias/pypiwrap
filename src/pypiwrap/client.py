from __future__ import annotations

import warnings
from xml.etree import ElementTree

import requests

from .consts import PYPI_HOST, SIMPLE_CONTENT_TYPE, SUPPORTED_SIMPLE_VERSION, USER_AGENT
from .exceptions import (
    ParseError,
    UnexpectedVersionWarning,
    UnsupportedVersionError,
    raise_for_status,
)
from .objects import IndexPage, Project, ProjectPage, PyPIFeed, Stats


class PyPIFeedClient:
    """Client for the PyPI RSS feeds.

    .. versionadded:: 2.0.0
    .. warning:: This client is only designed for hosts under the pypi.org domain.

    Arguments:
        host (str, optional):
            The base URL of the PyPI feeds host. Defaults to https://pypi.org.
    """

    def __init__(self, host=PYPI_HOST) -> None:
        self.host = host
        self.rest = requests.Session()
        self.rest.headers["User-Agent"] = USER_AGENT

    def __enter__(self):
        return self

    def __exit__(self, *exc_args) -> None:
        self.rest.close()

    def _get_feed(self, url: str) -> PyPIFeed:
        response = self.rest.get(url)
        raise_for_status(response)

        rss = ElementTree.fromstring(response.text)

        channel = rss.find("channel")

        if channel is None:
            raise ParseError("Could not parse RSS feed.")

        return PyPIFeed.from_xml(channel)

    def get_newest_packages(self) -> PyPIFeed:
        """Gets the newest packages created on PyPI."""
        return self._get_feed(f"{self.host}/rss/packages.xml")

    def get_latest_updates(self) -> PyPIFeed:
        """Gets the latest updates for individual projects on PyPI."""
        return self._get_feed(f"{self.host}/rss/updates.xml")

    def get_latest_releases_for_project(self, name: str) -> PyPIFeed:
        """Gets the latest releases for a project ``name``."""
        return self._get_feed(f"{self.host}/rss/project/{name}/releases.xml")


class PyPIClient:
    """Client for the PyPI JSON and Stats API.

    .. warning:: This client is only designed for hosts under the pypi.org domain.

    Arguments:
        host (str, optional):
            The base URL of the PyPI API host. Defaults to https://pypi.org.
    """

    def __init__(self, host=PYPI_HOST) -> None:
        self.host = host
        self.rest = requests.Session()
        self.rest.headers["User-Agent"] = USER_AGENT

    def __enter__(self):
        return self

    def __exit__(self, *exc_args) -> None:
        self.rest.close()

    def get_project(self, name: str, version: str | None = None) -> Project:
        """Gets information about a project or any of its releases.

        Arguments:
            name (str):
                The name of the project

            version (str):
                A version of the project to fetch. If none specified,
                the latest will be fetched.
        """

        if version:
            response = self.rest.get(f"{self.host}/pypi/{name}/{version}/json")
        else:
            response = self.rest.get(f"{self.host}/pypi/{name}/json")

        raise_for_status(
            response, {404: f"Could not find project or release for '{name}'"}
        )

        return Project.from_json(response.json())

    def get_stats(self) -> Stats:
        """Gets statistics about PyPI."""

        response = self.rest.get(
            f"{self.host}/stats", headers={"Accept": "application/json"}
        )
        raise_for_status(response)

        return Stats.from_json(response.json())


class SimpleRepoClient:
    """Client for the PyPI Simple Repository API (version 1).

    The methods included will emit a :class:`~.exceptions.UnexpectedVersionWarning`
    warning if it receives a response with a minor version greater than what's supported.

    As per PEP 629, the client will throw a :class:`~.exceptions.UnsupportedVersionError`
    exception if it receives a response with a major version greater than what's supported.

    Arguments:
        host (str, optional):
            The base URL of the Simple Repository API host. Defaults to https://pypi.org.
    """

    def __init__(self, host: str = PYPI_HOST) -> None:
        self.host = host
        self.rest = requests.Session()
        self.rest.headers["Accept"] = SIMPLE_CONTENT_TYPE
        self.rest.headers["User-Agent"] = USER_AGENT

    def __enter__(self):
        return self

    def __exit__(self, *exc_args) -> None:
        self.rest.close()

    def _verify_api_version(self, version: str) -> None:
        declared_major, declared_minor = [int(comp) for comp in version.split(".")]
        expected_major, expected_minor = SUPPORTED_SIMPLE_VERSION

        if declared_major > expected_major:
            raise UnsupportedVersionError(
                f"API response returned version {declared_major}.{declared_minor}, "
                f"expected major version {expected_major} or lower."
            )
        elif declared_major == expected_major and declared_minor > expected_minor:
            warnings.warn(
                f"API response returned version {declared_major}.{declared_minor}, "
                f"this version is not strictly supported (latest supported: "
                f"{expected_major}.{expected_minor}).",
                UnexpectedVersionWarning,
            )

    def get_index_page(self) -> IndexPage:
        """Gets the index page for this repository.

        .. warning::
            If you're using the PyPI host, the response returned by PyPI could
            take several seconds to parse. Please use this method sparingly.
        """

        response = self.rest.get(f"{self.host}/simple")
        raise_for_status(response)

        page = response.json()

        self._verify_api_version(page["meta"]["api-version"])
        return IndexPage.from_json(page)

    def get_project_page(self, project: str) -> ProjectPage:
        """Gets the project page for a given ``project``."""

        response = self.rest.get(f"{self.host}/simple/{project}")
        raise_for_status(response)

        page = response.json()

        self._verify_api_version(page["meta"]["api-version"])
        return ProjectPage.from_json(page)
