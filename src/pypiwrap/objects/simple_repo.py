from __future__ import annotations

from dataclasses import dataclass
from datetime import datetime

from ..utils import Size, iso_to_datetime, remove_additional
from .base import APIObject


@dataclass
class DistributionFile(APIObject):
    """A file representing a package distribution."""

    filename: str
    """The filename of this distribution."""

    url: str
    """The download URL for this file."""

    size: Size
    """The size of the distribution."""

    hashes: dict[str, str]
    """A mapping of hash names to hex encoded digests for this file."""

    upload_time: datetime | None = None
    """The upload time for this file."""

    requires_python: str | None = None
    """The version constraints for this file if specified.
    
    This is equivalent to the Requires-Python key in the Core metadata spec.
    """

    core_metadata: bool | dict[str, str] | None = None
    """
    An indication of whether metadata is available for this file.

    - If a boolean, whether this file has an associated metadata file.
    - If a dictionary, a mapping of hash names to hex encoded digests of the metadata file.
    - If None, this file has no associated metadata.
    """

    dist_info_metadata: bool | dict[str, str] | None = None
    """
    Contains the same values as :attr:`DistributionFile.core_metadata`. 
    
    When available, prefer using ``core_metadata`` over this attribute.
    """

    has_sig: bool | None = None  # API: gpg_sig
    """Whether a GPG signature for this file exists."""

    yanked: bool | str | None = None
    """
    - If a boolean, whether the file was yanked.
    - If a non-empty string, why the package was yanked.
    """

    @classmethod
    def from_raw(cls, data: dict) -> DistributionFile:
        # Certain API attributes, like requires-python, must be converted
        # to snake_case before unpacking
        result = {key.replace("-", "_"): val for key, val in data.items()}

        result["has_sig"] = result.get("gpg_sig")
        result["size"] = Size.from_int(result["size"])

        # See https://peps.python.org/pep-0714/ for why this is here.
        result["dist_info_metadata"] = result.pop("data_dist_info_metadata")

        if result.get("upload_time") is not None:
            result["upload_time"] = iso_to_datetime(result["upload_time"])

        return cls(**remove_additional(cls, result))

    def __repr__(self) -> str:
        return self._build_repr_string(self.filename, size=self.size.si)


@dataclass
class ProjectPage(APIObject):
    """A project page from the Index API."""

    name: str
    """The name of this project."""

    versions: list[str]
    """A list of all available versions for this project."""

    files: list[DistributionFile]
    """A list of distribution files for this project."""

    @classmethod
    def from_raw(cls, data: dict) -> ProjectPage:
        files = [DistributionFile.from_raw(pkg_file) for pkg_file in data["files"]]
        return cls(name=data["name"], versions=data["versions"], files=files)

    def __repr__(self) -> str:
        return self._build_repr_string(self.name)
