"""Module containing exceptions when communicating with the Netatmo API."""

from __future__ import annotations

from contextlib import contextmanager
from re import sub
from typing import Generator, Union

from httpx import (
    HTTPStatusError,
    NetworkError,
    Request,
    Response,
    TimeoutException,
    codes,
)


class UnsuportedArgumentsException(Exception):
    """Exception.

    Exception which is thrown when provided argument is not valid parameter of
    the method.
    """

    def __init__(self, message: str, **kwargs) -> None:
        """Init Function.

        Args:
            message: str
            **kwargs: Any
        """
        self.params = f"{kwargs=}"

        super().__init__(message, self.params)


class NonOkResponseException(Exception):
    """Exception.

    Exception which is thrown when server returns a valid HTTP response,
    but the request was not successfully handled and the response contains errors.
    """

    def __init__(self, message: str, **kwargs) -> None:
        """Init Function.

        Args:
            message: str
            **kwargs: Any
        """
        self.params = f"{kwargs=}"

        super().__init__(message, self.params)


class ApiException(Exception):
    """Base class for all exceptions related to networking."""

    def __init__(
        self, message: str, request: Request, response: Response | None
    ) -> None:
        """Init Function.

        Args:
            message: str
            request: Request
            response: Response
        """
        self.request = _sanitize_request(request)
        self.response = _sanitize_response(response)  # type: ignore

        super().__init__(message, self.request, self.response)


class RetryableException(ApiException):
    """Exception.

    Base class for all retryable exceptions related to networking.
    """


class NonRetryableException(ApiException):
    """Exception.

    Base class for all non-retryable exceptions related to networking.
    """


class NetworkTimeoutException(RetryableException):
    """Exception.

    Exception which is thrown when request times out and server doesn't
    return a response.
    """


class NetworkException(RetryableException):
    """Exception.

    Exception which is thrown when server is unavailable or unreachable
    and doesn't return a response.
    """


class RequestUnauthorizedException(NonRetryableException):
    """Exception.

    Exception which is thrown when server returns an 401 UNAUUTHORIZED or
    403 FORBIDDEN response.
    """


class RequestBackoffException(NonRetryableException):
    """Exception.

    Exception which is thrown when server returns an 429 TOO MANY REQUESTS
    response.
    """


class RequestClientException(NonRetryableException):
    """Exception which is thrown when server returns any 4xx response."""


class RequestServerException(RetryableException):
    """Exception which is thrown when server returns any 5xx response."""


class RequestException(RetryableException):
    """Exception which is thrown when server returns any other non-2xx response."""


@contextmanager
def client_error_handler() -> Generator[None]:  # type: ignore
    """Client error handler.

    Yields:
        error message

    Raises:
        NetworkException: description
        NetworkTimeoutException: description
        RequestBackoffException: description
        RequestClientException: description
        RequestException: description
        RequestServerException: description
        RequestUnauthorizedException: description
    """
    try:
        yield
    except TimeoutException as ex:
        raise NetworkTimeoutException(
            (
                "Request timed out while accessing the API. Retry the request with "
                "longer timeout. Check the network if the issue persists."
            ),
            ex.request,
            None,
        ) from ex
    except NetworkError as ex:
        raise NetworkException(
            (
                "Unknown network error while accessing the API."
                " Retry the request or check the network if the issue persists."
            ),
            ex.request,
            None,
        ) from ex
    except HTTPStatusError as ex:
        if ex.response.status_code in [codes.UNAUTHORIZED, codes.FORBIDDEN]:
            raise RequestUnauthorizedException(
                (
                    "Access token is invalid or expired. Refresh the access token"
                    "and try again."
                ),
                ex.request,
                ex.response,
            ) from ex
        if ex.response.status_code == codes.TOO_MANY_REQUESTS:
            raise RequestBackoffException(
                (
                    "Client is sending too many requests."
                    " Reduce the frequency at which API is accessed and try again."
                ),
                ex.request,
                ex.response,
            )
        if codes.is_client_error(ex.response.status_code):
            raise RequestClientException(
                (
                    "Server processed the request and returned a 4xx response."
                    " Don't retry the request without changing the arguments as the new"
                    " request will fail again with the same error."
                ),
                ex.request,
                ex.response,
            ) from ex
        if codes.is_server_error(ex.response.status_code):
            raise RequestServerException(
                (
                    "Server couldn't process the request successfully and returned a"
                    " 5xx response. Try again with reasonable backoff strategy."
                ),
                ex.request,
                ex.response,
            ) from ex

        raise RequestException(
            "Unknown response error. Check the log for more details.",
            ex.request,
            ex.response,
        ) from ex


def _sanitize_request(request: Request) -> Union[dict, None]:
    """Sanitize request.

    Args:
        request: Request object

    Returns:
        Request object sanitized
    """
    if not request:
        return None

    return {
        "method": request.method,
        "url": request.url,
        "headers": request.headers,
        "body": sub(
            rb"access_token=.+?(&|$)",
            rb"access_token=<FILTERED>&",
            sub(rb"password=.+?(&|$)", rb"password=<FILTERED>&", request.content),
        ),
    }


def _sanitize_response(response: Response) -> Union[dict, None]:
    if not response:
        return None

    return {
        "status_code": response.status_code,
        "url": response.url,
        "body": response.content,
        "duration": response.elapsed,
    }
