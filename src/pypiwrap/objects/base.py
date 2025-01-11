from __future__ import annotations

from typing import Any

from ..utils import remove_additional


class APIObject:
    """A base API object."""

    @classmethod
    def from_json(cls, data: dict[str, Any]) -> APIObject:
        return cls(**remove_additional(cls, data.copy()))

    def __init__(self, *args, **kwargs) -> None:
        super().__init__(*args, **kwargs)

    def _build_repr_string(self, *args, **kwargs) -> str:
        arg_string = " ".join(map(repr, args))
        kwarg_string = " ".join(f"{key}={value!r}" for key, value in kwargs.items())
        final_repr = (self.__class__.__name__, arg_string, kwarg_string)

        return "<" + " ".join(item for item in final_repr if item) + ">"
