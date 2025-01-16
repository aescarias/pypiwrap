from __future__ import annotations

from dataclasses import dataclass
from datetime import datetime
from typing import Any

from ..utils import Size, iso_to_datetime, remove_additional
from .base import APIObject


@dataclass
class Project(APIObject):
    """A PyPI project. This includes information about the project, its releases,
    and vulnerabilities."""

    author: str
    """The author of this project."""

    author_email: str
    """The email or contact details of the project's author."""

    dynamic: list[str]
    """A list of distribution metadata values marked as Dynamic.
    
    Dynamic values are values that are expected to be "filled in later" by build backends.
    See https://peps.python.org/pep-0643/ for details.
    """

    classifiers: list[str]
    """A list of PyPI classifiers for this project.
    
    See https://pypi.org/classifiers for a complete list of classifiers.
    """

    description: str
    """A description of the project."""

    description_content_type: str | None
    """The content type of the description if available.
    
    PyPI supports 3 content types: ``text/plain``, ``text/x-rst`` (reStructuredText), and
    ``text/markdown``. PyPI will default to RST if no content type is specified or to
    plain text if the content type is invalid.
    """

    docs_url: str | None
    """The documentation URL for the project if available."""

    home_page: str
    """The project's home page."""

    keywords: str | None
    """Keywords relating to this project."""

    license: str
    """Text indicating the license for this project."""

    license_expression: str | None
    """If present, a valid SPDX license expression."""

    license_files: list[str]
    """A list of licenses attached to the project, if any."""

    maintainer: str | None
    """The project's maintainer."""

    maintainer_email: str | None
    """The email or contact details of the project's maintainer."""

    name: str
    """The name of the project."""

    package_url: str
    """The PyPI package URL.
     
    The :attr:`.project_url` attribute should be preferred. Please see docs for details."""

    platform: str | None
    """The release's platform target if any specified.
    
    Usually, this is only set for platforms not included in the PyPI classifiers."""

    project_urls: dict[str, str]
    """A mapping of labels to URLs relating to the project."""

    project_url: str
    """The PyPI project's URL.
    
    :attr:`.package_url` and :attr:`.project_url` are effectively the same value. Users
    should prefer this attribute.

    See https://github.com/pypi/warehouse/issues/3206 for details.
    """

    release_url: str
    """The project URL relating to this specific release."""

    requires_dist: list[str]
    """A list of required distributions or dependencies specified according to PEP 508."""

    requires_python: str | None
    """The Python version required for this release."""

    provides_extra: list[str]
    """A list of optional or extra features provided by the package.
    
    See https://peps.python.org/pep-0566/ for details. Distribution extra names should be 
    valid Python identifiers as defined in https://peps.python.org/pep-0685/.
    """

    summary: str
    """A short summary of the project."""

    version: str
    """The version of the project."""

    yanked: bool
    """Whether this release was 'yanked' or removed from circulation."""

    yanked_reason: str | None
    """The reason the release was yanked if applicable."""

    file_urls: list[ReleaseFile]
    """A list of files for this release."""

    vulnerabilities: list[Vulnerability]
    """A list of vulnerabilities for this release, if any."""

    last_serial: int
    """The most recent serial ID number for this project."""

    @classmethod
    def from_json(cls, data: dict[str, Any]) -> Project:
        info = remove_additional(cls, data["info"].copy())

        info["requires_dist"] = info.get("requires_dist") or []
        info["provides_extra"] = info.get("provides_extra") or []
        info["dynamic"] = info.get("dynamic") or []
        info["license_files"] = info.get("license_files") or []

        vulns = list(map(Vulnerability.from_json, data["vulnerabilities"]))
        files = list(map(ReleaseFile.from_json, data["urls"]))

        return cls(
            **info,
            last_serial=data["last_serial"],
            vulnerabilities=vulns,
            file_urls=files,
        )

    def __repr__(self) -> str:
        return self._build_repr_string(
            self.name,
            summary=self.summary,
            version=self.version,
            package_url=self.package_url,
        )


@dataclass
class Vulnerability(APIObject):
    """A vulnerability in a project or release."""

    aliases: list[str]
    """The identifiers used to refer to this vulnerability."""

    details: str
    """Details about this vulnerability."""

    fixed_in: list[str]
    """A list of releases where this vulnerability was addressed."""

    id: str
    """An identifier for this vulnerability."""

    link: str
    """A URL where more information about this vulnerability is provided."""

    source: str
    """The source from where this vulnerability report was obtained."""

    summary: str | None
    """A short summary of this vulnerability if available."""

    withdrawn: datetime | None = None
    """The datetime this vulnerability was withdrawn if applicable."""

    @classmethod
    def from_json(cls, data: dict[str, Any]) -> Vulnerability:
        if data.get("withdrawn") is not None:
            data["withdrawn"] = iso_to_datetime(data["withdrawn"])

        return cls(**remove_additional(cls, data))

    def __repr__(self) -> str:
        return self._build_repr_string(
            id=self.id, source=self.source, withdrawn=self.withdrawn
        )


@dataclass
class ReleaseFile(APIObject):
    """A file part of a PyPI release."""

    digests: dict[str, str]
    """A mapping of hash names to hex encoded digests corresponding to this release file.

    Usually, the digests available are ``md5``, ``sha256``, and ``blake2b_256``. 
    The keys available should be members of :attr:`hashlib.algorithms_guaranteed`.
    """

    filename: str
    """The filename for this release file."""

    package_type: str  # API: packagetype
    """The package type of this file. 
    
    Package types are grouped into 'sdist' for source distributions and 'bdist_*' for
    built distributions.
    
    As of PEP 527 and PEP 715, PyPI only accepts 'sdist' and 'bdist_wheel'. Other bdist 
    variants may still be returned for older packages but they are considered legacy 
    and can no longer be uploaded to PyPI.
    """

    python_version: str
    """The Python version target for this file.
    
    This value is 'source' for source distributions and a version target following 
    PEP 425 for built distributions.
    """

    requires_python: str
    """The Python version constraints for this file. 
    
    This is equivalent to the 'Requires-Python' key in the Core metadata specification.
    """

    size: Size
    """The size of this release file."""

    upload_time: datetime
    """The time this file was uploaded on."""

    upload_time_tz: datetime  # API: upload_time_iso_8601
    """The time this file was uploaded on in UTC and compliant with ISO 8601."""

    url: str
    """The URL for this release file."""

    yanked: bool
    """Whether this package was yanked."""

    yanked_reason: str | None
    """Why the package was yanked if applicable."""

    @classmethod
    def from_json(cls, data: dict[str, Any]) -> ReleaseFile:
        data = data.copy()

        # Converting values to appropriate types
        data["size"] = Size.from_int(data["size"])
        data["upload_time_iso_8601"] = iso_to_datetime(data["upload_time_iso_8601"])
        data["upload_time"] = datetime.fromisoformat(data["upload_time"])

        # Renaming values to appropriate
        data["upload_time_tz"] = data.pop("upload_time_iso_8601")
        data["package_type"] = data.pop("packagetype")

        return cls(**remove_additional(cls, data))

    def __repr__(self) -> str:
        return self._build_repr_string(
            self.filename, size=self.size.si, package_type=self.package_type
        )


@dataclass
class Stats(APIObject):
    """Statistics about PyPI."""

    total_size: Size
    """The total size of all packages on PyPI combined."""

    top_packages: dict[str, Size]
    """A mapping of top packages sorted by size."""

    @classmethod
    def from_json(cls, data: dict[str, Any]) -> Stats:
        sorted_packages = sorted(
            data["top_packages"].items(), key=lambda item: item[1]["size"]
        )

        top_packages = {
            name: Size.from_int(package["size"]) for name, package in sorted_packages
        }

        return cls(
            total_size=Size.from_int(data["total_packages_size"]),
            top_packages=top_packages,
        )

    def __repr__(self) -> str:
        return self._build_repr_string(total_size=self.total_size.si)
