from __future__ import annotations
import requests

def error_from_response(
    rs: requests.Response, 
    messages: dict[int, str] | None = None
) -> ClientError:
    if messages is None:
        messages = {}

    error_map = {
        404: NotFound
    }

    exc = error_map.get(rs.status_code, ClientError)

    return exc(rs.status_code, messages.get(rs.status_code, rs.reason))


class ClientError(Exception):
    """Exception raised if an error occurred while performing a request through the client."""
    def __init__(self, status: int, reason: str) -> None:
        self.status = status
        self.reason = reason

        super().__init__(f"{status}: {reason}")


class NotFound(ClientError):
    """Exception raised when a project, release, or file was not found"""
    pass
