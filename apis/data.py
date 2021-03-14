# Imports
from typing import Union
import requests
from . import _shared

# Exceptions
class PackageNotFound(Exception):
    """
    Exception raised when a requested package was not found.
    """
    def __init__(self, package):
        super().__init__(f"Package '{package}' was not found.")


class VersionNotFound(Exception):
    """
    Exception raised when a requested version of a package was not found.
    """
    def __init__(self, package, version):
        super().__init__(f"Version '{version}' for package '{package}' was not found.")


# Classes
class MainAPI:
    """
    Python class that handles requests to the PyPi API for use in other
    PyPiWrap classes.
    """
    def __init__(self, package: str):
        self.package: str = package
        self.url: str = f"https://pypi.org/pypi/{package}/json"
        self.req: requests.Response = requests.get(self.url)
        
        # If package not found, raise exception
        if self.req.status_code == 404:
            raise PackageNotFound(package)

        self.json: dict = self.req.json()


class PackageInfo:
    """
    Package information provided by the API
    """
    def __init__(self, package: str):
        self.requested_package: str = package
        
        # API init
        api_instance = MainAPI(self.requested_package)
        api_json: dict = api_instance.json
        
        # Raw package info
        self.package_info: dict = api_json["info"]
        pkg_info = self.package_info
        
        # Author
        self.author: str = pkg_info["author"]
        self.author_email: str = pkg_info["author_email"]
        
        # Varied data
        self.bugtrack_url: str = pkg_info["bugtrack_url"]
        self.classifiers: list = pkg_info["classifiers"]
        
        # Description
        self.description: str = pkg_info["description"]
        self.description_content_type: str = pkg_info["description_content_type"]
        
        # Docs and downloads
        self.docs_url: str = pkg_info["docs_url"]
        self.download_url: str = pkg_info["download_url"]
        self.downloads: dict = pkg_info["downloads"]
        
        # More varied data 
        self.home_page: str = pkg_info["home_page"]
        self.keywords: str = pkg_info["keywords"]
        self.license: str = pkg_info["license"]
        
        # Maintainer
        self.maintainer: str = pkg_info["maintainer"]
        self.maintainer_emaiL: str = pkg_info["maintainer_email"]
        
        # Package and URLs
        self.name: str = pkg_info["name"]
        self.package_name: str = self.name
        self.package_url = pkg_info["package_url"]
        self.platform: str = pkg_info["platform"]
        self.project_url: str = pkg_info["project_url"]
        self.project_urls: dict = pkg_info["project_urls"]
        self.release_url: str = pkg_info["release_url"]
        
        # Dependencies
        self.requires_dist: list = pkg_info["requires_dist"]
        self.dependencies: list = self.requires_dist
        self.requires_python: str = pkg_info["requires_python"]

        # Package summary
        self.summary: str = pkg_info["summary"]

        # Package version data
        self.version: str = pkg_info["version"]
        self.latest_version: str = self.version
        self.package_version: str = self.version
        self.available_versions: list = [rel for rel in api_json["releases"]]
        
        # Yanked releases
        self.yanked: bool = pkg_info["yanked"]
        self.yanked_reason: str = pkg_info["yanked_reason"]
    
    def __repr__(self):
        return f"Package(name='{self.name}', version='{self.version}', author='{self.author}', summary='{self.summary}')"


class ReleaseFile:
    """
    Release file created by ReleaseInfo; used for storing file information
    """
    def __new__(cls, data: dict, module=None):
        if not isinstance(module, ReleaseInfo):
            raise RuntimeError(f"Cannot create '{cls.__module__}.{cls.__name__}' instances.")
        return object.__new__(cls)

    def __init__(self, data: dict, module=None):
        self.release_data: dict = data
        rel_data = self.release_data

        # Varied data 
        self.comment_text: str = rel_data["comment_text"]
        self.digests: dict = rel_data["digests"]
        self.downloads: int = rel_data["downloads"]
        self.filename: str = rel_data["filename"]
        self.file_name = self.filename

        # Signatures
        self.has_sig: bool = rel_data["has_sig"]
        self.has_signatures = self.has_sig
        self.md5_digest: str = rel_data["md5_digest"]
        
        # Package type
        self.packagetype: str = rel_data["packagetype"]
        self.package_type = self.packagetype

        # Python version
        self.python_version: str = rel_data["python_version"]
        self.requires_python: str = rel_data["requires_python"]

        # File size
        self.size: int = rel_data["size"]
        self.file_size_bytes: int = self.size
        self.file_size_readable: str = _shared.convert_bytes_to_readable(self.size)
        self.file_size_readable_iec: str = _shared.convert_bytes_to_readable(self.size, True)
        
        # Upload time
        self.upload_time: str = rel_data["upload_time"]
        self.upload_time_iso_8601: str = rel_data["upload_time_iso_8601"]

        # URL
        self.url: str = rel_data["url"]
        self.file_url = self.url

        # Yanked
        self.yanked: bool = rel_data["yanked"]
        self.yanked_reason: str = rel_data["yanked_reason"]


    def __repr__(self):
        return f"File(name='{self.filename}', type='{self.packagetype}', size='{self.file_size_readable}', url='{self.url}')"


class ReleaseInfo:
    """
    Release information of a package provided by the API
    """
    def __build_filename(self, files):
        file_info = []
        for file in files:
            file_info.append(ReleaseFile({
                "comment_text" : file["comment_text"],
                "digests" : file["digests"],
                "downloads" : file["downloads"],
                "filename" : file["filename"],
                "has_sig" : file["has_sig"],
                "md5_digest" : file["md5_digest"],
                "packagetype" : file["packagetype"],
                "python_version" : file["python_version"],
                "requires_python" : file["requires_python"],
                "size" : file["size"],
                "upload_time" : file["upload_time"],
                "upload_time_iso_8601" : file["upload_time_iso_8601"],
                "url" : file["url"],
                "yanked" : file["yanked"],
                "yanked_reason" : file["yanked_reason"] 
            }, module=self))
        return file_info
         
    def __init__(self, package: str, version: Union[str, list, None] = None, skip_not_found: bool = False):
        self.requested_package: str = package
        self.requested_version: Union[str, list, None] = version
        version = self.requested_version

        # API init
        api_instance = MainAPI(self.requested_package)
        api_json: dict = api_instance.json

        # Package info
        self.release_info: dict = api_json["releases"]
        rel_info = self.release_info

        self.available_versions: list = [rel for rel in rel_info]
        self.available_releases: list = self.available_versions
        self.version_data: dict = {}

        if version is None:
            for ver in rel_info:
                info = rel_info[ver]
                self.version_data[ver] = self.__build_filename(info)
        elif isinstance(version, list):
            for ver in version:
                if ver not in self.available_versions:
                    if not skip_not_found:
                        raise VersionNotFound(api_json["info"]["name"], ver)                     
                else:    
                    info = rel_info[ver]
                    self.version_data[ver] = self.__build_filename(info)
        elif isinstance(version, str):
            if version not in self.available_versions:
                raise VersionNotFound(api_json["info"]["name"], version)
            self.version_data[version] = self.__build_filename(rel_info[version])