from __future__ import annotations
from datetime import datetime

from dataclasses import dataclass

from pypiwrap.utils import Size, remove_additional, iso_to_datetime


class Base:
    """The base class for other pypiwrap objects"""
    
    @classmethod
    def from_raw(cls, data: dict):
        data = data.copy()
        return cls(**remove_additional(cls, data))
    
    def __init__(self, *args, **kwargs) -> None:
        super().__init__(*args, **kwargs)


@dataclass
class Package(Base):
    """A PyPi package"""

    author: str
    """The author of the package"""

    author_email: str
    """The email of the package's author"""

    bugtrack_url: str | None
    """A bug tracking URL if available"""

    classifiers: list[str]
    """A list of PyPi classifiers for the package"""

    description: str
    """A description of the package"""
    
    description_content_type: str | None
    """The content type of the description if available"""

    docs_url: str | None
    """The documentation for the package if available"""

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
    """The name of the package"""

    package_url: str
    """The PyPi package URL"""

    platform: str | None
    """The platform for which this package is designed for, if any specifically"""

    project_urls: dict[str, str]
    """A mapping of URLs relating to the project"""

    project_url: str
    """The project URL of the package"""

    release_url: str
    """The project URL relating to this specific release"""

    requires_dist: str | None
    """A list of required distributions or dependencies"""

    requires_python: str | None
    """The version required for the package"""

    summary: str
    """A short summary of the package"""

    version: str
    """The version of the package"""

    yanked: bool
    """Whether his package was 'yanked' or removed from circulation"""

    yanked_reason: str | None
    """If available, the reason for the yanking of the package"""

    file_urls: list[ReleaseURL]
    """A list of file URLs for this package"""

    vulnerabilities: list[Vulnerability]
    """A list of vulnerabilities for this package if any"""

    last_serial: int

    @classmethod
    def from_raw(cls, data: dict) -> Package:
        data = data.copy()
        info = remove_additional(cls, data["info"])

        vulns = map(Vulnerability.from_raw, data["vulnerabilities"])
        files = map(ReleaseURL.from_raw, data["urls"])

        return Package(
            **info,
            last_serial=data["last_serial"],
            vulnerabilities=[*vulns],
            file_urls=[*files]
        )

    def __repr__(self) -> str:
        return f"<Package '{self.name}' summary='{self.summary}' " \
               f"version='{self.version}' package_url='{self.package_url}'>"


@dataclass
class ReleaseURL(Base):
    comment_text: str
    """A comment for this release"""

    digests: dict[str, str]
    """A mapping of hashes corresponding to this release file"""
    
    # downloads: int
    filename: str
    """The filename for this release file"""
   
    has_sig: bool
    """Whether this release file has a PGP signature attached to it"""

    md5_digest: str
    """An MD5 digest of the release file"""

    packagetype: str
    """The type of release file. It can be either of:
    - ``sdist``: A source distribution (generally a .tar.gz file)
    - ``bdist_*``: A built distribution (generally a wheel or egg file)
    """

    python_version: str
    """A general Python version for this package"""

    requires_python: str
    """The required version constraints for this file"""

    size: Size
    """The size of the release file"""

    upload_time: datetime
    """The time this file was uploaded on"""
    
    upload_time_tz: datetime # API: upload_time_iso_8601
    """The time this file was uploaded on in UTC and compliant with IS0 8601"""

    url: str
    """The URL for this release file"""

    yanked: bool
    """Whether this package has been yanked"""

    yanked_reason: str | None
    """If the package was yanked, the reason for such"""

    @classmethod
    def from_raw(cls, data: dict) -> ReleaseURL:
        data = data.copy()
        # Converting values to appropriate ones
        data["size"] = Size.from_bytes(data["size"])
        data["upload_time_iso_8601"] = iso_to_datetime(data["upload_time_iso_8601"])
        data["upload_time"] = datetime.fromisoformat(data["upload_time"])

        # Renaming values to appropriate
        data["upload_time_tz"] = data.pop("upload_time_iso_8601")
        
        data.pop("downloads")
        return ReleaseURL(**data)


    def __repr__(self) -> str:
        return f"<ReleaseURL filename='{self.filename}' size='{self.size.si}' " \
               f"packagetype='{self.packagetype}'>"


@dataclass
class Vulnerability(Base):
    """A package vulnerability"""

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
        return f"<Vulnerability id='{self.id}' source='{self.source}'>"


@dataclass
class PackageFile(Base):
    filename: str
    """The filename of the package file"""

    url: str
    """The download URL for the file"""

    hashes: dict[str, str]
    """A mapping of common hashes for the file"""

    requires_python: str | None = None
    """If specified, the version constraints for this file"""

    dist_info_metadata: bool | dict[str, str] | None = None
    """
    - If a boolean, whether the file has associated metadata
    - If a dictionary, a mapping of hashes to encoded metadata hashes
    """

    gpg_sig: bool | None = None
    """Whether a GPG signature is included with the file"""

    yanked: bool | str | None = None
    """
    - If a boolean, represents whether the file was yanked
    - If a string, represents the yanking reason
    """

    @classmethod
    def from_raw(cls, data: dict) -> PackageFile:
        # Certain API attributes, like requires-python, must be converted
        # to snake_case before unpacking
        result = { k.replace("-", "_"): v for k, v in data.items() }
        return PackageFile(**result)

    def __repr__(self) -> str:
        return f"<PackageFile '{self.filename}' url='{self.url}'>"


@dataclass
class Stats(Base):
    """Dataclass for PyPi statistics"""

    total_size: Size
    """The current size of all packages on PyPi combined"""

    top_packages: dict[str, Size]
    """The packages with the largest sizes"""

    @classmethod
    def from_raw(cls, data: dict) -> Stats:
        size = Size.from_bytes(data["total_packages_size"])
        pkgs = { 
            k: Size.from_bytes(v["size"]) 
            for k, v in data["top_packages"].items() 
        }
 
        return Stats(size, pkgs)
        
