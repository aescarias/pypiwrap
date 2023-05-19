from __future__ import annotations

import dataclasses
from datetime import datetime
from typing import NamedTuple, Any

import requests

SI_SUFFIXES  = ["B", "KB", "MB", "GB", "TB"]
IEC_SUFFIXES = ["B", "KiB", "MiB", "GiB", "TiB"]


class Size(NamedTuple):
    """A tuple that includes human-readable representations of a file size"""

    bytes: int
    """The size represented in bytes"""
    iec: str
    """The size represented in binary/IEC units (KiB, MiB)"""
    si: str
    """The size represented in decimal/SI units (KB, MB)"""

    @classmethod
    def from_int(cls, num: int) -> Size:
        return Size(
            num, 
            iec=bytes_to_readable(num, 'iec'), 
            si=bytes_to_readable(num, 'si')
        )

    def __int__(self) -> int:
        return self.bytes


def iso_to_datetime(iso: str) -> datetime:
    """Convert an ISO 8601 string to a datetime object"""
    return datetime.strptime(iso, "%Y-%m-%dT%H:%M:%S.%f%z")

def gpg_from_url(url: str) -> str | None:
    """Gets the GPG signature of a file from its URL if available"""

    rs = requests.get(url + ".asc")
    if rs.ok:
        return rs.text

# where unit is either of 'si' or 'iec'
def bytes_to_readable(num: float, unit: str = 'si') -> str:
    """Converts a number (in bytes) to a human-readable string representation"""
    if unit == 'iec':
        suffixes = IEC_SUFFIXES
        step_unit = 1024
    else:
        suffixes = SI_SUFFIXES
        step_unit = 1000

    # last one is assumed to be greatest
    suffix = None
    for suffix in suffixes:
        if num < step_unit:
            break
        num /= step_unit
    
    return f"{num:.2f} {suffix or suffixes[-1]}"

def remove_additional(cls: type[Any], data: dict[str, Any]) -> dict[str, Any]:
    """Takes any dataclass and a dictionary that can unpack to it
    and strips any additional keys not part of the dataclass"""

    result = data.copy()
    names = [field.name for field in dataclasses.fields(cls)]

    for key in data:
        if key not in names:
            result.pop(key)

    return result
