"""Module HTTP communication with the OpenMotics API."""

from .errors import (
    ApiException,
    NetworkException,
    NetworkTimeoutException,
    NonOkResponseException,
    NonRetryableException,
    RequestBackoffException,
    RequestClientException,
    RequestException,
    RequestServerException,
    RequestUnauthorizedException,
    RetryableException,
    UnsuportedArgumentsException,
)
from .openmotics import CloudClient, LocalGatewayClient  # openmotics_client,

__all__ = [
    "CloudClient",
    "LocalGatewayClient",
    "ApiException",
    "NonOkResponseException",
    "NetworkException",
    "NetworkTimeoutException",
    "NonRetryableException",
    "RequestBackoffException",
    "RequestClientException",
    "RequestException",
    "RequestServerException",
    "RequestUnauthorizedException",
    "RetryableException",
    "UnsuportedArgumentsException",
    "openmotics_client",
]
