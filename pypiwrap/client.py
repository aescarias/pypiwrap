from __future__ import annotations
from typing import Generator

import requests

from pypiwrap import objects

JSON_URL = "https://pypi.org/pypi"
STATS_URL = "https://pypi.org/stats"
SIMPLE_URL = "https://pypi.org/simple"

CONTENT_TYPE = "application/vnd.pypi.simple.v1+json"


class ClientError(Exception):
    """A general PyPi client exception, serves as the base for other exceptions"""
    pass


class NotFound(ClientError):
    """Exception raised when a package or specific version was not found"""
    pass
        
    
class PyPiClient:
    """Client interface to the PyPi APIs

    All methods here are expected to raise a :class:`ClientError` or any of its subclasses in case it was unable
    to retrieve information due to an error.
    """
    def __init__(self) -> None:
        self.rest = requests.Session()
    
    def get_package(self, name: str, version: str | None = None) -> objects.Package:
        """Gets information about a package or any of its specific versions.
        
        Arguments:
            name (:class:`str`): The name of the package
            
            version (:class:`str`, optional):
                The version to get specific information about. If not specified,
                the latest version will be assumed.

        Raises:
            :class:`NotFound` - The package or version was found.

            :class:`ClientError` - The client was unable to retrieve the package due to an error.
        """
        
        if version:
            rs = self.rest.get(f"{JSON_URL}/{name}/{version}/json")
        else:
            rs = self.rest.get(f"{JSON_URL}/{name}/json")

        if not rs.ok:
            if rs.status_code == 404:
                raise NotFound(f"Could not find package '{name}' or its version")   
            raise ClientError(f"{rs.status_code} {rs.reason}")

        return objects.Package.from_raw(rs.json())
    
    def get_all_projects(self) -> Generator[str, None, None]:
        """Yields a list of names for all the projects available on PyPi"""
        rs = self.rest.get(SIMPLE_URL, headers={ "Accept": CONTENT_TYPE })        

        if not rs.ok:
            raise ClientError(f"{rs.status_code} {rs.reason}")

        projects = rs.json()["projects"]

        for proj in projects:
            yield proj["name"]

    def get_files(self, name: str) -> list[objects.PackageFile]:
        """Gets the files for a package. Returns a list of package files."""
        rs = self.rest.get(f"{SIMPLE_URL}/{name}", headers={ "Accept": CONTENT_TYPE })
        
        if not rs.ok:
            raise ClientError(f"{rs.status_code} {rs.reason}")

        files = rs.json()["files"]

        return list(map(objects.PackageFile.from_raw, files))

    def get_stats(self) -> objects.Stats:
        """Gets statistics about the PyPi registry"""

        rs = self.rest.get(STATS_URL, headers={
            "Accept": "application/json"
        })
        
        if not rs.ok:
            raise ClientError(f"{rs.status_code} {rs.reason}")
        
        return objects.Stats.from_raw(rs.json())
