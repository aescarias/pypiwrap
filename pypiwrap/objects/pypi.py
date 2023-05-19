from __future__ import annotations
from dataclasses import dataclass
from datetime import datetime
from typing import Any

from .base import APIObject
from ..utils import Size, iso_to_datetime, remove_additional
    

@dataclass
class Project(APIObject):
    """A PyPi project"""

    author: str
    """The author of the project"""

    author_email: str
    """The email of the project's author"""

    bugtrack_url: str | None
    """A bug tracking URL if available"""

    classifiers: list[str]
    """A list of PyPi [classifiers](https://pypi.org/classifiers) for this project"""

    description: str
    """A description of the project"""
    
    description_content_type: str | None
    """The content type of the description if available"""

    docs_url: str | None
    """The documentation URL for the project if available"""

    download_url: str
    """The project's download URL"""

    home_page: str
    """The project's home page"""

    keywords: str
    """Keywords relating to this project"""

    license: str
    """The license for this project"""

    maintainer: str
    """The project's maintainer"""

    maintainer_email: str
    """The email of the project's maintainer"""

    name: str
    """The name of the project"""

    package_url: str
    """The PyPi package URL"""

    platform: str | None
    """The release's platform target if any specified"""

    project_urls: dict[str, str]
    """A mapping of labels to URLs relating to the project"""

    project_url: str
    """The PyPi project's URL"""

    release_url: str
    """The project URL relating to this specific release"""

    requires_dist: list[str]
    """A list of required distributions or dependencies in a format similar to a requirements file"""

    requires_python: str | None
    """The Python version required for this release"""

    summary: str
    """A short summary of the project"""

    version: str
    """The version of the project"""

    yanked: bool
    """Whether this release was 'yanked' or removed from circulation"""

    yanked_reason: str | None
    """The reason the release was yanked if applicable"""

    file_urls: list[ReleaseFile]
    """A list of files for this release"""

    vulnerabilities: list[Vulnerability]
    """A list of vulnerabilities for this release if any"""

    last_serial: int

    @classmethod
    def _from_raw(cls, data: dict) -> Project:
        info = remove_additional(cls, data["info"].copy())

        vulns = list(map(Vulnerability._from_raw, data["vulnerabilities"]))
        files = list(map(ReleaseFile._from_raw, data["urls"]))

        if not data["info"].get("requires_dist"):
            data["info"]["requires_dist"] = []

        return cls(**info,
            last_serial=data["last_serial"],
            vulnerabilities=vulns,
            file_urls=files
        )

    def __repr__(self) -> str:
        return self._build_repr(self.name, 
            summary=self.summary, 
            version=self.version, 
            package_url=self.package_url
        )


@dataclass
class Vulnerability(APIObject):
    """A vulnerability in a project or release"""

    aliases: list[str]
    """The names used to refer to this vulnerability"""

    details: str
    """Details about the vulnerability"""

    fixed_in: list[str]
    """Releases where this vulnerability was fixed"""

    id: str
    """Identifier for this vulnerability"""
    
    link: str
    """An URL where more information is provided about the vulnerability"""
    
    source: str
    """The source from where this vulnerability report was obtained"""

    summary: str | None
    """A short summary of the vulnerability if available"""

    withdrawn: datetime | None = None
    """The datetime this vulnerability was withdrawn"""

    @classmethod
    def _from_raw(cls, data: dict) -> Vulnerability:
        if data.get("withdrawn") is not None:
            data["withdrawn"] = iso_to_datetime(data["withdrawn"])

        return cls(**remove_additional(cls, data))
    
    def __repr__(self) -> str:
        return self._build_repr(id=self.id, source=self.source, withdrawn=self.withdrawn)
    

@dataclass
class ReleaseFile(APIObject):
    """A file part of a release"""

    comment_text: str
    """A comment for this release"""

    digests: dict[str, str]
    """A mapping of hashes corresponding to this release file.

    Most commonly, the digests available are ``md5``, ``sha256``, and ``blake2b_256``. 
    The keys available must be members of :attr:`hashlib.algorithms_guaranteed`.
    """
    
    # downloads: int
    # md5_digest: str

    filename: str
    """The filename for this release file"""
   
    has_sig: bool
    """Whether this release file has a PGP signature attached to it"""

    package_type: str  # API: packagetype
    """The type of release file. It can be either of:
    
    - ``sdist``: A source distribution (generally a .tar.gz file)
    - ``bdist_*``: A built distribution where `*` is either `wheel` or `egg`
    """

    python_version: str
    """The general Python version target for this file.
    
    It is `source` for source distributions and a version target for built distributions.
    """

    requires_python: str
    """The Python version constraints for this file"""

    size: Size
    """The size of the release file"""

    upload_time: datetime
    """The time this file was uploaded on"""
    
    upload_time_tz: datetime # API: upload_time_iso_8601
    """The time this file was uploaded on in UTC and compliant with ISO 8601"""

    url: str
    """The URL for this release file"""

    yanked: bool
    """Whether this package was yanked"""

    yanked_reason: str | None
    """Why the package was yanked if applicable"""

    @classmethod
    def _from_raw(cls, data: dict) -> ReleaseFile:
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
        return self._build_repr(self.filename, 
            size=self.size.si, 
            package_type=self.package_type
        )


@dataclass
class Stats(APIObject):
    """Statistics about PyPI"""

    total_size: Size
    """The total size of all packages on PyPI combined"""
    
    top_packages: dict[str, Size]
    """Mapping of top packages sorted by size"""
    
    @classmethod
    def _from_raw(cls, data: dict[str, Any]) -> Stats:
        top_pkgs_sort = sorted(data["top_packages"].items(), 
                               key=lambda it: it[1]["size"])

        top_pkgs = { name: Size.from_int(pkg["size"]) for name, pkg in top_pkgs_sort } 
        
        return cls(
            total_size=Size.from_int(data["total_packages_size"]),
            top_packages=top_pkgs   
        )
    
    def __repr__(self) -> str:
        return self._build_repr(total_size=self.total_size.si)
