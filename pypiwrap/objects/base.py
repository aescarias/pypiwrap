from __future__ import annotations

from ..utils import remove_additional


class APIObject:
    """A base API object"""
    
    @classmethod
    def _from_raw(cls, data: dict) -> APIObject:
        return cls(**remove_additional(cls, data.copy()))
    
    def __init__(self, *args, **kwargs) -> None:
        super().__init__(*args, **kwargs)

    def _build_repr(self, *args, **kwargs) -> str:
        arg_string = " ".join(map(repr, args))
        kwarg_string = " ".join(f"{k}={repr(v)}" for k, v in kwargs.items())
        final = (self.__class__.__name__, arg_string, kwarg_string)

        return "<" + ' '.join(filter(None, final)).strip() + ">"
