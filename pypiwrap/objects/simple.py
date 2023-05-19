from __future__ import annotations
from dataclasses import dataclass
from datetime import datetime

from .base import APIObject
from ..utils import Size, iso_to_datetime, remove_additional


@dataclass
class DistributionFile(APIObject):
    """A file for a package distribution"""

    filename: str
    """The filename of the distribution"""

    url: str
    """The download URL for the file"""

    size: Size
    """The size of the distribution"""

    hashes: dict[str, str]
    """A mapping of hashes for this file. Similar to :attr:`ReleaseFile.digests`."""

    upload_time: datetime | None = None
    """The upload time for this file"""

    requires_python: str | None = None
    """The version constraints for this file if specified"""

    dist_info_metadata: bool | dict[str, str] | None = None
    """
    - If a boolean, whether this file has associated metadata.
    - If a dictionary, a mapping of hashes to encoded metadata file hashes.
    """

    has_sig: bool | None = None  # API: gpg_sig
    """Whether a GPG signature is included with the file"""

    yanked: bool | str | None = None
    """
    - If a boolean, whether the file was yanked.
    - If a string, why the package was yanked.
    """

    @classmethod
    def _from_raw(cls, data: dict) -> DistributionFile:
        # Certain API attributes, like requires-python, must be converted
        # to snake_case before unpacking
        result = { k.replace("-", "_"): v for k, v in data.items() }
        
        result["has_sig"] = result.get("gpg_sig")
        result["size"] = Size.from_int(result["size"])
        result["dist_info_metadata"] = result.pop("data_dist_info_metadata")

        if result.get("upload_time") is not None:
            result["upload_time"] = iso_to_datetime(result["upload_time"])

        return cls(**remove_additional(cls, result))
        
    def __repr__(self) -> str:
        return self._build_repr(self.filename, size=self.size.si)


@dataclass
class ProjectPage(APIObject):
    """A Simple project page"""

    name: str
    """The name of the project"""
    
    versions: list[str]
    """A list of all available versions of the project"""
    
    files: list[DistributionFile]
    """A list of distribution files for the project"""

    @classmethod
    def _from_raw(cls, data: dict) -> ProjectPage:
        files = [DistributionFile._from_raw(fl) for fl in data["files"]]
        return cls(name=data["name"], versions=data["versions"], files=files)

    def __repr__(self) -> str:
        return self._build_repr(self.name)
