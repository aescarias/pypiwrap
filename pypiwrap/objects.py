from __future__ import annotations

from datetime import datetime
from dataclasses import dataclass

from . import utils 
from .utils import Size


class Base:
    """The base class for other pypiwrap objects"""
    
    @classmethod
    def _from_raw(cls, data: dict):
        return cls(**utils.remove_additional(cls, data.copy()))
    
    def __init__(self, *args, **kwargs) -> None:
        super().__init__(*args, **kwargs)

    def _build_repr(self, *args, **kwargs) -> str:
        arg_string = " ".join(map(repr, args))
        kwarg_string = " ".join(f"{k}={repr(v)}" for k, v in kwargs.items())
        final = (self.__class__.__name__, arg_string, kwarg_string)

        return "<" + ' '.join(filter(None, final)).strip() + ">"
    

@dataclass
class Project(Base):
    """A PyPi project"""

    author: str
    """The author of the project"""

    author_email: str
    """The email of the project's author"""

    bugtrack_url: str | None
    """A bug tracking URL if available"""

    classifiers: list[str]
    """A list of PyPi classifiers for the project.
    Valid values are provided at https://pypi.org/classifiers.
    """

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
    """The release's platform target if any specifically"""

    project_urls: dict[str, str]
    """A mapping of URLs relating to the project"""

    project_url: str
    """The PyPi project's URL"""

    release_url: str
    """The project URL relating to this specific release"""

    requires_dist: list[str]
    """A list of required distributions or dependencies in a format similar to a requirements file"""

    requires_python: str | None
    """The version required for this release"""

    summary: str
    """A short summary of the project"""

    version: str
    """The version of the project"""

    yanked: bool
    """Whether this release was 'yanked' or removed from circulation"""

    yanked_reason: str | None
    """The reason the release was yanked if applicable"""

    file_urls: list[ReleaseFile]
    """A list of file URLs for this release"""

    vulnerabilities: list[Vulnerability]
    """A list of vulnerabilities for this release if any"""

    last_serial: int

    @classmethod
    def _from_raw(cls, data: dict) -> Project:
        data = data.copy()
        info = utils.remove_additional(cls, data["info"])

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
class ReleaseFile(Base):
    """A file part of a release"""

    comment_text: str
    """A comment for this release"""

    digests: dict[str, str]
    """A mapping of hashes corresponding to this release file.

    The keys available can vary but should always members of ``hashlib.algorithms_guaranteed``
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
    - ``bdist_*``: A built distribution where `*` is generally `wheel` or `egg`
    """

    python_version: str
    """The general Python version target for this file.
    
    It is `source` for source distributions and a version target for built distributions.
    """

    requires_python: str
    """The required version constraints for this file"""

    size: Size
    """The size of the release file"""

    upload_time: datetime
    """The time this file was uploaded on"""
    
    upload_time_tz: datetime # API: upload_time_iso_8601
    """The time this file was uploaded on in a format compliant with ISO 8601 and in UTC"""

    url: str
    """The URL for this release file"""

    yanked: bool
    """Whether this package has been yanked"""

    yanked_reason: str | None
    """If the package was yanked, the reason for such"""

    @classmethod
    def _from_raw(cls, data: dict) -> ReleaseFile:
        data = data.copy()

        # Converting values to appropriate types
        data["size"] = Size.from_bytes(data["size"])
        data["upload_time_iso_8601"] = utils.iso_to_datetime(data["upload_time_iso_8601"])
        data["upload_time"] = datetime.fromisoformat(data["upload_time"])

        # Renaming values to appropriate
        data["upload_time_tz"] = data.pop("upload_time_iso_8601")
        data["package_type"] = data.pop("packagetype")

        # Remove unneeded/unimplemented
        data = utils.remove_additional(cls, data)
        return cls(**data)

    def __repr__(self) -> str:
        return self._build_repr(self.filename, 
            size=self.size.si, 
            package_type=self.package_type
        )


@dataclass
class Vulnerability(Base):
    """A vulnerability in a project or release"""

    aliases: str
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

    def __repr__(self) -> str:
        return self._build_repr(id=self.id, source=self.source)


@dataclass
class DistributionFile(Base):
    """A file for a package distribution"""

    filename: str
    """The filename of the distribution"""

    url: str
    """The download URL for the file"""

    hashes: dict[str, str]
    """A mapping of common hashes for the file. Similar to :attr:`ReleaseFile.digests`."""

    requires_python: str | None = None
    """If specified, the version constraints for this file"""

    dist_info_metadata: bool | dict[str, str] | None = None
    """
    - If a boolean, whether this file has associated metadata
    - If a dictionary, a mapping of hashes to encoded metadata file hashes
    """

    has_sig: bool | None = None  # API: gpg_sig
    """Whether a GPG signature is included with the file"""

    yanked: bool | str | None = None
    """
    - If a boolean, represents whether the file was yanked
    - If a string, represents the yanking reason
    """

    @classmethod
    def _from_raw(cls, data: dict) -> DistributionFile:
        # Certain API attributes, like requires-python, must be converted
        # to snake_case before unpacking
        result = { k.replace("-", "_"): v for k, v in data.items() }
        result["has_sig"] = result.get("gpg_sig")

        return cls(**utils.remove_additional(cls, result))

    def __repr__(self) -> str:
        return self._build_repr(self.filename, url=self.url)


@dataclass
class Stats(Base):
    """A PyPi statistics object. It currently only stores the top packages by size."""

    total_size: Size
    """The current size of all packages on PyPi combined"""

    top_packages: dict[str, Size]
    """The packages with the largest sizes"""

    @classmethod
    def _from_raw(cls, data: dict) -> Stats:
        size = Size.from_bytes(data["total_packages_size"])
        pkgs = { 
            k: Size.from_bytes(v["size"]) 
            for k, v in data["top_packages"].items() 
        }
 
        return cls(size, pkgs)
    
    def __repr__(self) -> str:
        return self._build_repr(total_size=self.total_size)
