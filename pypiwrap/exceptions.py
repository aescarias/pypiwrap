from __future__ import annotations
import requests

def raise_for_status(
    rs: requests.Response, 
    messages: dict[int, str] | None = None
) -> None:
    """Raises an exception based on the response's status code.
    If the status code is deemed OK, this will do nothing.
    
    Args:
        rs (:class:`requests.Response`): The response itself.

        messages (:class:`dict[int, str]`, optional):
            An *optional* mapping of status codes to messages.        
    """
    if rs.ok:
        return
    
    if messages is None:
        messages = {}

    error_map = { 404: NotFound }

    exc = error_map.get(rs.status_code, ClientError)
    raise exc(rs.status_code, messages.get(rs.status_code, rs.reason))


class ClientError(Exception):
    """Raised when an error occurs while performing a request."""
    def __init__(self, status: int, reason: str) -> None:
        self.status = status
        self.reason = reason

        super().__init__(f"{status}: {reason}")


class NotFound(ClientError):
    """Raised when a project, release, or file was not found"""
    pass
