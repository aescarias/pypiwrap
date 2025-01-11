from __future__ import annotations

import requests

from ._version import __version__
from .exceptions import raise_for_status
from .objects import IndexPage, Project, ProjectPage, Stats

PYPI_HOST = "https://pypi.org"
SIMPLE_CONTENT_TYPE = "application/vnd.pypi.simple.v1+json"
USER_AGENT = f"aescarias/pypiwrap {__version__}"


class PyPIClient:
    """Client for the PyPI JSON and Stats API."""

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
            name (:class:`str`): The name of the project

            version (:class:`str`, optional):
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

        return Project.from_raw(response.json())

    def get_stats(self) -> Stats:
        """Gets statistics about PyPI."""

        response = self.rest.get(
            f"{self.host}/stats", headers={"Accept": "application/json"}
        )
        raise_for_status(response)

        return Stats.from_raw(response.json())


class SimpleRepoClient:
    """Client for the PyPI Simple Repository API."""

    def __init__(self, host: str = PYPI_HOST) -> None:
        self.host = host
        self.rest = requests.Session()
        self.rest.headers["Accept"] = SIMPLE_CONTENT_TYPE
        self.rest.headers["User-Agent"] = USER_AGENT

    def __enter__(self):
        return self

    def __exit__(self, *exc_args) -> None:
        self.rest.close()

    def get_index_page(self) -> IndexPage:
        """Gets the index page for this repository."""

        response = self.rest.get(f"{self.host}/simple")
        raise_for_status(response)

        return IndexPage.from_raw(response.json())

    def get_project_page(self, project: str) -> ProjectPage:
        """Gets the page for a given ``project``."""

        response = self.rest.get(f"{self.host}/simple/{project}")
        raise_for_status(response)

        return ProjectPage.from_raw(response.json())
