import requests
from . import _shared


# Classes
class TopPackage:
    """
    Package created by Statistics; used for storing top package information
    """
    def __new__(cls, data: dict, module=None):
        if not isinstance(module, Statistics):
            raise RuntimeError(f"Cannot create '{cls.__module__}.{cls.__name__}' instances.")
        return object.__new__(cls)
        
    def __init__(self, data: dict, module=None):
        self.package_data: dict = data
        pkg_data = self.package_data

        self.name = pkg_data["name"]
        self.package_name = self.name

        self.size = pkg_data["size"]
        self.package_size = self.size
        self.package_size_readable: str = _shared.convert_bytes_to_readable(self.size)
        self.package_size_readable_iec: str = _shared.convert_bytes_to_readable(self.size, True)
        
    def __repr__(self):
        return f"TopPackage(name='{self.name}', size='{self.package_size_readable}')"


class Statistics:
    """
    Statistics related to PyPi packages
    """
    def __init__(self):
        url: str = "https://pypi.org/stats/"
        req: requests.Response = requests.get(url, headers={
            "Accept" : "application/json"
        })
        self.json: dict = req.json()
        self.top_packages: dict = self.json["top_packages"]

        self.stats: list = []
        self.total_packages_size: int = self.json["total_packages_size"]
        total_size: int = self.total_packages_size
        
        self.total_packages_size_readable: str = _shared.convert_bytes_to_readable(total_size)
        self.total_packages_size_readable_iec: str = _shared.convert_bytes_to_readable(total_size, True)

        for stat in self.top_packages:
            self.stats.append(TopPackage({
                "name" : stat,
                "size" : self.top_packages[stat]["size"]
            }, module=self))
            