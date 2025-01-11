from __future__ import annotations

import dataclasses
from datetime import datetime
from typing import Any, Literal, NamedTuple

SI_SUFFIXES = ["B", "KB", "MB", "GB", "TB"]
IEC_SUFFIXES = ["B", "KiB", "MiB", "GiB", "TiB"]


class Size(NamedTuple):
    """A tuple that includes human-readable representations of a file size."""

    bytes: int
    """The size represented in bytes."""

    iec: str
    """The size represented in binary/IEC units (KiB, MiB)."""

    si: str
    """The size represented in decimal/SI units (KB, MB)."""

    @classmethod
    def from_int(cls, num: int) -> Size:
        return Size(
            num, iec=bytes_to_readable(num, "iec"), si=bytes_to_readable(num, "si")
        )

    def __int__(self) -> int:
        return self.bytes


def iso_to_datetime(iso: str) -> datetime:
    """Converts an ISO 8601 string to a datetime object."""

    try:
        return datetime.strptime(iso, "%Y-%m-%dT%H:%M:%S.%f%z")
    except ValueError:
        return datetime.strptime(iso, "%Y-%m-%dT%H:%M:%S%z")


def bytes_to_readable(number: float, unit: Literal["si", "iec"] = "si") -> str:
    """Converts a number (in bytes) to a human-readable string representation.

    Arguments:
        number (:class:`float`):
            A value in bytes.

        unit (:class:`str`, optional):
            Units to use when representing the result. May be ``si`` for decimal (MB) units
            which is the default or ``iec`` for binary (MiB) units.
    """
    if unit == "iec":
        suffixes = IEC_SUFFIXES
        step_unit = 1024
    else:
        suffixes = SI_SUFFIXES
        step_unit = 1000

    # last one is assumed to be greatest
    suffix = None
    for suffix in suffixes:
        if number < step_unit:
            break
        number /= step_unit

    return f"{number:.2f} {suffix or suffixes[-1]}"


def remove_additional(cls: type[Any], data: dict[str, Any]) -> dict[str, Any]:
    """Takes any dataclass ``cls`` and a dictionary ``data`` that can unpack to
    it and discards any additional keys not part of the dataclass.

    Returns:
        A ``dict`` that can safely unpack to the dataclass.
    """

    result = data.copy()
    names = [field.name for field in dataclasses.fields(cls)]

    for key in data:
        if key not in names:
            result.pop(key)

    return result
