from __future__ import annotations
from typing import Generator, Any

import requests

from . import exceptions, objects

JSON_URL = "https://pypi.org/pypi"
STATS_URL = "https://pypi.org/stats"

SIMPLE_URL = "https://pypi.org/simple"
SIMPLE_CONTENT_TYPE = "application/vnd.pypi.simple.v1+json"

USER_AGENT = "pypiwrap/1.0.0 (github: aescarias)"


class PyPIClient:
    """Client for the PyPI JSON and Stats API"""

    def __init__(self) -> None:
        self.rest = requests.Session()
        self.rest.headers["User-Agent"] = USER_AGENT

    def __enter__(self):
        return self

    def __exit__(self, *args):
        self.rest.close()

    def get_project(self, name: str, version: str | None = None) -> objects.Project:
        """Gets information about a project or any of its specific releases.
        
        Arguments:
            name (:class:`str`): The name of the project
            
            version (:class:`str`, optional):
                A specific version of the project. If none specified,
                the latest is assumed.
        """
        
        if version:
            rs = self.rest.get(f"{JSON_URL}/{name}/{version}/json")
        else:
            rs = self.rest.get(f"{JSON_URL}/{name}/json")
        
        exceptions.raise_for_status(rs, {
            404: f"Could not find project or release for '{name}'"
        })
        
        return objects.Project._from_raw(rs.json())

    def get_stats(self) -> objects.Stats:
        """Gets statistics about PyPI"""
        
        rs = self.rest.get("https://pypi.org/stats", 
                           headers={ "Accept": "application/json"})
        exceptions.raise_for_status(rs)

        return objects.Stats._from_raw(rs.json())


class SimpleClient:
    """Client for the PyPI Simple API"""

    def __init__(self) -> None:
        self.rest = requests.Session()
        self.rest.headers["Accept"] = SIMPLE_CONTENT_TYPE
        self.rest.headers["User-Agent"] = USER_AGENT

    def __enter__(self):
        return self

    def __exit__(self, *args):
        self.rest.close()
    
    def get_index(self) -> Generator[str, None, None]:
        """Yields a list of all projects registered on PyPI"""
        rs = self.rest.get(SIMPLE_URL)
        exceptions.raise_for_status(rs)

        for project in rs.json()["projects"]:
            yield project["name"]

    def get_page(self, project: str) -> objects.ProjectPage:
        """Gets a specific page for a project"""
        rs = self.rest.get(f"{SIMPLE_URL}/{project}")
        exceptions.raise_for_status(rs)
        
        return objects.ProjectPage._from_raw(rs.json())
