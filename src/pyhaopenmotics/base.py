"""Module containing a BaseClient for the OpenMotics API."""
from __future__ import annotations

import logging
from typing import TYPE_CHECKING, Any

import cached_property
from httpx import URL, AsyncClient, Response
from tenacity import (
    retry,
    retry_if_exception_type,
    stop_after_attempt,
    stop_after_delay,
    wait_random_exponential,
)

from .const import CLOUD_HOST, PREFIX
from .devices.groupactions import GroupActionsCtrl
from .devices.installations import InstallationsCtrl
from .devices.outputs import OutputsCtrl
from .devices.shutters import ShuttersCtrl
from .errors import RetryableException, client_error_handler

logger = logging.getLogger(__name__)


class BaseClient:
    """
    Base client for making HTTP requests to the OpenMotics API.

    Uses the constructor provided AsyncClient and Auth from httpx to make
    authenticated requests. The provided AsyncClient should be used as a
    singleton for making all requests to allow efficient connection pool management.
    """

    def __init__(
        self,
        host: str | None = None,
        ssl: bool | None = True,
        port: int | None = 443,
    ) -> None:
        """
        Create new base client instance.

        Uses the provided parameters when making API calls towards the
        OpenMotics API.
        """

        self._client = None
        self._session: AsyncClient = None
        self._close_session = False

        if host is None:
            self._host = CLOUD_HOST
        else:
            self._host = host

        self.url = "{}://{}:{}".format("https" if ssl else "http", self._host, port)
        self.token_url = self._get_url("/authentication/oauth2/token")

        self.installations = InstallationsCtrl(baseclient=self)
        self.outputs = OutputsCtrl(baseclient=self)
        self.shutters = ShuttersCtrl(baseclient=self)
        self.groupactions = GroupActionsCtrl(baseclient=self)

    def _get_url(self, endpoint):
        """Join endpoint to url."""
        return "{}{}{}".format(self.url, PREFIX, endpoint)

    @retry(
        retry=retry_if_exception_type(RetryableException),
        stop=(stop_after_delay(300) | stop_after_attempt(10)),
        wait=wait_random_exponential(multiplier=1, max=30),
        reraise=True,
    )
    async def _post(self, path: str, data: dict, **kwargs) -> Any:
        """
        Makes post request using the underlying httpx AsyncClient, with the defaut timeout of 15s.

        In case of retryable exceptions, requests are retryed for up to 10 times or 5 minutes.
        """
        uri = self._get_url(path)

        with client_error_handler():
            resp = await self._session.post(
                uri,
                data=data,
                timeout=15.0,
                **kwargs,
            )

            resp.raise_for_status()

        if "application/json" in resp.headers.get("Content-Type", ""):
            response_data = resp.json()
            return response_data

        return resp.text()

    @retry(
        retry=retry_if_exception_type(RetryableException),
        stop=(stop_after_delay(300) | stop_after_attempt(10)),
        wait=wait_random_exponential(multiplier=1, max=30),
        reraise=True,
    )
    async def _get(self, path: str, **kwargs) -> Any:
        """
        Makes get request using the underlying httpx AsyncClient, with the defaut timeout of 15s.

        In case of retryable exceptions, requests are retryed for up to 10 times or 5 minutes.
        """
        uri = self._get_url(path)

        self.headers = {
            "Accept": "application/json",
            # "Content-Type": "application/json"
        }
        # self._client.headers.update(self.headers)

        with client_error_handler():
            resp = await self._session.get(
                uri,
                timeout=15.0,
                headers=self.headers,
                **kwargs,
            )

            resp.raise_for_status()

        if "application/json" in resp.headers.get("Content-Type", ""):
            response_data = resp.json()
            return response_data
        return resp.text()

    async def close(self) -> None:
        """Close open client session."""
        if self._session and self._close_session:
            await self._session.aclose()

    async def __aenter__(self) -> Toon:
        """Async enter."""
        return self

    async def __aexit__(self, *exc_info) -> None:
        """Async exit."""
        await self.close()
