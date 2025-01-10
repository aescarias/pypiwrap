from __future__ import annotations

import requests


def raise_for_status(
    response: requests.Response, messages: dict[int, str] | None = None
) -> None:
    """Raises an exception based on the response's status code. If the status code is
    deemed OK, this will do nothing.

    Arguments:
        response (:class:`requests.Response`): The response itself.

        messages (:class:`dict[int, str]`, optional):
            An optional mapping of status codes to messages.
    """
    if response.ok:
        return

    if messages is None:
        messages = {}

    error_map = {404: NotFound}

    exc = error_map.get(response.status_code, ClientError)
    raise exc(response.status_code, messages.get(response.status_code, response.reason))


class ClientError(Exception):
    """Raised when an error occurs while performing a request."""

    def __init__(self, status: int, reason: str) -> None:
        self.status = status
        self.reason = reason

        super().__init__(f"{status}: {reason}")


class NotFound(ClientError):
    """Raised when a project, release, or file was not found."""

    pass
