from __future__ import annotations

from dataclasses import dataclass
from datetime import datetime
from enum import Enum
from typing import Any

from ..utils import Size, iso_to_datetime, remove_additional
from .base import APIObject


class ProjectStatus(str, Enum):
    """The project status marker as documented by PEP 792.

    See https://peps.python.org/pep-0792/ for details.

    .. versionadded:: 2.1.0
    """

    ACTIVE = "active"
    """The project is active. This is the default status."""

    ARCHIVED = "archived"
    """The project does not expect to be updated in the future."""

    QUARANTINED = "quarantined"
    """The project is considered generally unsafe to use, e.g. due to malware."""

    DEPRECATED = "deprecated"
    """The project is considered obsolete, and may have been superseded by another project."""


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
    
    This is equivalent to the 'Requires-Python' key in the Core metadata spec.
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

    provenance_url: str | None = None  # API: provenance
    """If available, a URL to the file's associated provenance.
    
    See https://peps.python.org/pep-0740/#provenance-objects for details.
    
    .. versionadded:: 2.0.0
    """

    has_gpg_sig: bool | None = None  # API: gpg_sig
    """Whether a GPG signature for this file exists. If none, this value is unknown.
    
    For PyPI/Warehouse, this will always return None as GPG signatures are no longer
    supported by the service.
    """

    yanked: bool | str | None = None
    """
    - If a boolean, whether the file was yanked.
    - If a non-empty string, why the package was yanked.
    """

    @classmethod
    def from_json(cls, data: dict[str, Any]) -> DistributionFile:
        # Certain API attributes, like requires-python, must be converted
        # to snake_case before unpacking
        result = {key.replace("-", "_"): val for key, val in data.items()}

        result["has_gpg_sig"] = result.get("gpg_sig")
        result["size"] = Size.from_int(result["size"])

        # See https://peps.python.org/pep-0714/ for why this is here.
        result["dist_info_metadata"] = result.pop("data_dist_info_metadata", None)

        result["provenance_url"] = result.pop("provenance", None)

        if result.get("upload_time") is not None:
            result["upload_time"] = iso_to_datetime(result["upload_time"])

        return cls(**remove_additional(cls, result))

    @property
    def gpg_url(self) -> str | None:
        """If available, a URL containing the GPG signature for this file."""
        if self.has_gpg_sig:
            return self.url + ".asc"

    @property
    def metadata_url(self) -> str | None:
        """If available, a URL containing the metadata file."""
        if self.core_metadata or self.dist_info_metadata:
            return self.url + ".metadata"

    def __repr__(self) -> str:
        return self._build_repr_string(self.filename, size=self.size.si)


@dataclass
class Meta(APIObject):
    """Information about a response from the Simple Repository API.

    .. versionadded:: 2.0.0
    """

    api_version: str
    """The API version being implemented. 
    
    See https://peps.python.org/pep-0629/ for details.
    """

    tracks: list[str]
    """If a repository, a list of project/repository URLs being "tracked" by the 
    extending repository.
    
    See https://peps.python.org/pep-0708/#repository-tracks-metadata for details.
    """

    project_status: ProjectStatus = ProjectStatus.ACTIVE
    """The project status marker as described in PEP 792. See :class:`.ProjectStatus`
    for details on possible values. The default value is :attr:`.ProjectStatus.ACTIVE`.

    .. versionadded:: 2.1.0
    """

    project_status_reason: str | None = None
    """The reason or description of the project status marker, if any.
    
    .. versionadded:: 2.1.0
    """

    @classmethod
    def from_json(cls, data: dict[str, Any]) -> Meta:
        return Meta(
            api_version=data["api-version"],
            tracks=data.get("tracks", []),
            project_status=ProjectStatus(
                data.get("project-status", ProjectStatus.ACTIVE)
            ),
            project_status_reason=data.get("project-status-reason"),
        )

    def __repr__(self) -> str:
        return self._build_repr_string(api_version=self.api_version)


@dataclass
class IndexPage(APIObject):
    """The index page of the Simple Repository API.

    .. versionadded:: 2.0.0
    """

    meta: Meta
    """Information about the response."""

    projects: list[str]
    """A list of projects in the index."""

    @classmethod
    def from_json(cls, data: dict[str, Any]) -> IndexPage:
        return cls(
            meta=Meta.from_json(data["meta"]),
            projects=[proj["name"] for proj in data["projects"]],
        )

    def __repr__(self) -> str:
        return self._build_repr_string(self.meta.api_version)


@dataclass
class ProjectPage(APIObject):
    """A project page from the Simple Repository API."""

    meta: Meta
    """Information about the response.

    .. versionadded:: 2.0.0
    """

    name: str
    """The name of this project."""

    alternate_locations: list[str]
    """A list of alternate locations or namespaces for this project. 
    
    See https://peps.python.org/pep-0708/#alternate-locations-metadata for details.
    
    .. versionadded:: 2.0.0
    """

    versions: list[str]
    """A list of all available versions for this project."""

    files: list[DistributionFile]
    """A list of distribution files for this project."""

    @classmethod
    def from_json(cls, data: dict[str, Any]) -> ProjectPage:
        files = [DistributionFile.from_json(pkg_file) for pkg_file in data["files"]]

        return cls(
            meta=Meta.from_json(data["meta"]),
            name=data["name"],
            alternate_locations=data.get("alternate-locations", []),
            versions=data["versions"],
            files=files,
        )

    def __repr__(self) -> str:
        return self._build_repr_string(self.name)
