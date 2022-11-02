from __future__ import annotations
from typing import Generator

import requests

from . import objects, exceptions

JSON_URL = "https://pypi.org/pypi"
STATS_URL = "https://pypi.org/stats"
SIMPLE_URL = "https://pypi.org/simple"

CONTENT_TYPE = "application/vnd.pypi.simple.v1+json"
        
    
class Client:
    """Client interface to the PyPi APIs

    All methods here are expected to raise a :class:`~.exceptions.ClientError` or any of its subclasses 
    in case it was unable to retrieve information due to an error.

    For example:
        >>> import pypiwrap
        >>> wrap = pypiwrap.Client()
        >>> rope = wrap.get_project("rope", "1.4.0")
        >>> print(rope.summary)
        'a python refactoring library...'

    """
    def __init__(self) -> None:
        self.rest = requests.Session()
    
    def get_project(self, name: str, version: str | None = None) -> objects.Project:
        """Gets information about a project or any of its specific versions.
        
        Arguments:
            name (:class:`str`): The name of the project
            
            version (:class:`str`, optional):
                The version to get specific information about. If not specified,
                the latest version will be assumed.

        Raises:
            :class:`~.exceptions.NotFound` - The project or version was not found.

            :class:`~.exceptions.ClientError` - The client was unable to retrieve the project due to an error.
        """
        
        if version:
            rs = self.rest.get(f"{JSON_URL}/{name}/{version}/json")
        else:
            rs = self.rest.get(f"{JSON_URL}/{name}/json")

        if not rs.ok:
            raise exceptions.error_from_response(rs, {
                404: f"Could not find project or release for '{name}'"
            })
        
        return objects.Project._from_raw(rs.json())
    
    def get_all_projects(self) -> Generator[str, None, None]:
        """Yields a list of names for all the projects available on PyPi"""
        rs = self.rest.get(SIMPLE_URL, headers={ "Accept": CONTENT_TYPE })        

        if not rs.ok:
            raise exceptions.error_from_response(rs)

        projects = rs.json()["projects"]

        for proj in projects:
            yield proj["name"]

    def get_files(self, name: str) -> list[objects.DistributionFile]:
        """Gets the file distributions for a package."""
        rs = self.rest.get(f"{SIMPLE_URL}/{name}", headers={ "Accept": CONTENT_TYPE })
        
        if not rs.ok:
            raise exceptions.error_from_response(rs, {
                404: f"Could not find project '{name}'"
            })
        
        files = rs.json()["files"]

        return list(map(objects.DistributionFile._from_raw, files))

    def get_stats(self) -> objects.Stats:
        """Gets statistics about the PyPi registry"""

        rs = self.rest.get(STATS_URL, headers={
            "Accept": "application/json"
        })
        
        if not rs.ok:
            raise exceptions.error_from_response(rs)
        
        return objects.Stats._from_raw(rs.json())
