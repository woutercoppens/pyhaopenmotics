"""Module containing a ThermostatClient for the Netatmo API."""

from __future__ import annotations

from authlib.integrations.httpx_client import (  # type: ignore
    AsyncOAuth2Client,
    OAuthError,
)
from oauthlib.oauth2 import (  # type: ignore
    BackendApplicationClient,
    LegacyApplicationClient,
)

from .base import BaseClient
from .errors import ApiException, RequestUnauthorizedException


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

        self.token = None

    async def token_saver(self, token, **kwargs):
        """Save the token to self.token.

        Args:
            token: str
            **kwargs: any
        """
        self.token = token

    async def get_token(self):
        """Get a new token.

        Raises:
            RequestUnauthorizedException: blabla
            ApiException: blabla
        """
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
                f"API: {exc}",
                None,
                None,
            ) from exc

        return


class LocalGatewayClient(BaseClient):
    """Doc String."""

    # NOT TESTED
    def __init__(self, host, username, password, port=443, ssl=True, **kwargs):
        """Init the LegacyClient object.

        Args:
            host: str
            username: str
            password: str
            port: int
            ssl: bool
            **kwargs: other arguments
        """
        super().__init__(host=host, **kwargs)

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

        self.token = None

    async def get_token(self):
        """Get a new token.

        Raises:
            RequestUnauthorizedException: blabla
            ApiException: blabla
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
                f"API: {exc}",
                None,
                None,
            ) from exc

        return

    async def token_saver(self, token, **kwargs):
        """Save the token to self.token.

        Args:
            token: str
            **kwargs: any
        """
        self.token = token
