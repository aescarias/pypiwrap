from __future__ import annotations
from typing import Generator, Any

import requests

from . import exceptions, objects

PYPI_HOST = "https://pypi.org" 
SIMPLE_CONTENT_TYPE = "application/vnd.pypi.simple.v1+json"
USER_AGENT = "pypiwrap/1.0.0 (github: aescarias)"

#? The constants below are marked for potential deprecation.
JSON_URL = f"{PYPI_HOST}/pypi"
STATS_URL = f"{PYPI_HOST}/stats"
SIMPLE_URL = f"{PYPI_HOST}/simple"


class PyPIClient:
    """Client for the PyPI JSON and Stats API"""

    def __init__(self, host=PYPI_HOST) -> None:
        self.host = host
        self.rest = requests.Session()
        self.rest.headers["User-Agent"] = USER_AGENT

    def __enter__(self):
        return self

    def __exit__(self, *args):
        self.rest.close()

    def get_project(self, name: str, version: str | None = None) -> objects.Project:
        """Gets information about a project or any of its releases.
        
        Arguments:
            name (:class:`str`): The name of the project
            
            version (:class:`str`, optional):
                A version of the project to fetch. If none specified,
                the latest will be fetched.
        """
        
        if version:
            rs = self.rest.get(f"{self.host}/pypi/{name}/{version}/json")
        else:
            rs = self.rest.get(f"{self.host}/pypi/{name}/json")
        
        exceptions.raise_for_status(rs, {
            404: f"Could not find project or release for '{name}'"
        })
        
        return objects.Project._from_raw(rs.json())

    def get_stats(self) -> objects.Stats:
        """Gets statistics about PyPI"""
        
        rs = self.rest.get(f"{self.host}/stats", 
                           headers={ "Accept": "application/json"})
        exceptions.raise_for_status(rs)

        return objects.Stats._from_raw(rs.json())


class SimpleClient:
    """Client for the PyPI Simple API"""

    def __init__(self, host: str = PYPI_HOST) -> None:
        self.host = host
        self.rest = requests.Session()
        self.rest.headers["Accept"] = SIMPLE_CONTENT_TYPE
        self.rest.headers["User-Agent"] = USER_AGENT

    def __enter__(self):
        return self

    def __exit__(self, *args):
        self.rest.close()
    
    def get_index(self) -> Generator[str, None, None]:
        """Yields a list of names for all projects registered on this repository"""
        rs = self.rest.get(f"{self.host}/simple")
        exceptions.raise_for_status(rs)

        for project in rs.json()["projects"]:
            yield project["name"]

    def get_page(self, project: str) -> objects.ProjectPage:
        """Gets the page for a given project"""
        rs = self.rest.get(f"{self.host}/simple/{project}")
        exceptions.raise_for_status(rs)
        
        return objects.ProjectPage._from_raw(rs.json())
