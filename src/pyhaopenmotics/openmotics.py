"""Module containing a ThermostatClient for the Netatmo API."""

from __future__ import annotations

import json
from contextlib import asynccontextmanager
from datetime import datetime
from enum import Enum
from typing import AsyncGenerator, Callable, Dict, Union

from authlib.integrations.httpx_client import (
    AsyncAssertionClient,
    AsyncOAuth2Client,
    OAuthError,
)
from httpx import AsyncClient
from oauthlib.oauth2 import (
    BackendApplicationClient,
    LegacyApplicationClient,
    ServiceApplicationClient,
)

from .base import BaseClient
from .errors import ApiException, RequestUnauthorizedException

# @asynccontextmanager
# async def openmotics_client(
#     client_id: str,
#     client_secret: str,
#     token: Token,
#     on_token_update: Callable[[Token], None],
# ) -> AsyncGenerator[OutputsClient, None]:
#     client = AsyncClient()
#     token_store = Union[
#         CloudTokenStore(client_id, client_secret, token, on_token_update),
#         LocalTokenStore(username, password, token, on_token_update),
#     ]

#     c = OpenMoticsClient(client, token_store)

#     try:
#         yield c
#     finally:
#         await client.aclose()


class CloudClient(BaseClient):
    """Docstring."""

    def __init__(self, client_id, client_secret, **kwargs):
        """Init the BackendClient object.

        Args:
            client_id: str
            client_secret: str
            **kwargs: other arguments
        """
        super().__init__(**kwargs)

        self.client_id = client_id
        self.client_secret = client_secret
        self.scope = "control view"

        self._client = BackendApplicationClient(client_id=self.client_id)
        self._session = AsyncOAuth2Client(  # noqa: S106
            client_id=self.client_id,
            client_secret=self.client_secret,
            token_endpoint_auth_method="client_secret_post",  # nosec
            scope=self.scope,
            token_endpoint=self.token_url,
            grant_type="client_credentials",
            update_token=self.token_saver,
        )

    def token_saver(self, token, **kwargs):
        """Save the token to self.token.

        Args:
            token: str
            **kwargs: any
        """
        self.token = token

    async def get_token(self):
        """Get a new token.

        Raises:
            OpenMoticsAuthenticationError: blabla
            OpenMoticsError: blabla
        """
        print(self.token_url)
        try:
            self.token = await self._session.fetch_token(
                url=self.token_url,
                grant_type="client_credentials",
            )
        except OAuthError as exc:
            raise RequestUnauthorizedException(
                f"Error occurred while communicating with the OpenMotics API: {exc}"
            ) from exc
        except Exception as exc:  # pylint: disable=broad-except
            raise ApiException(
                f"Unknown error occurred while communicating with the OpenMotics "
                f"API: {exc}"
            ) from exc

        return


class LocalGatewayClient(BaseClient):
    """Doc String."""

    # NOT TESTED
    def __init__(self, username, password, **kwargs):
        """Init the LegacyClient object.

        Args:
            username: str
            password: str
            **kwargs: other arguments
        """
        super().__init__(**kwargs)

        self.username = username
        self.password = password
        self.scope = "control view"
        self._client = LegacyApplicationClient(client_id="Legacy")

        self._session = AsyncOAuth2Client(  # noqa: S106
            username=self.username,
            password=self.password,
            token_endpoint_auth_method="client_secret_basic",  # nosec
            scope=self.scope,
            token_endpoint=self.token_url,
            grant_type="client_credentials",
            update_token=self.token_saver,
        )

    async def get_token(self):
        """Get a new token.

        Raises:
            OpenMoticsAuthenticationError: blabla
            OpenMoticsError: blabla
        """
        try:
            self.token = await self._session.fetch_token(
                url=self.token_url,
                username=self.username,
                password=self.password,
            )
        except OAuthError as exc:
            raise RequestUnauthorizedException(
                f"Error occurred while communicating with the OpenMotics API: {exc}"
            ) from exc
        except Exception as exc:  # pylint: disable=broad-except
            raise ApiException(
                f"Unknown error occurred while communicating with the OpenMotics "
                f"API: {exc}"
            ) from exc

        return

    def token_saver(self, token, **kwargs):
        """Save the token to self.token.

        Args:
            token: str
            **kwargs: any
        """
        self.token = token
