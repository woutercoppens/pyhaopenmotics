"""Module containing the base of an installation."""

from __future__ import annotations

from typing import TYPE_CHECKING, List

from pyhaopenmotics.models.installation import Installation

if TYPE_CHECKING:
    from pyhaopenmotics.base import BaseClient  # pylint: disable=R0401


class InstallationsCtrl:  # noqa: SIM119
    """Object holding information of the OpenMotics installation.

    All actions related to Installations or a specific Installation.
    """

    def __init__(self, baseclient: BaseClient) -> None:
        """Init the installations object.

        Args:
            baseclient: BaseClient
        """
        self.baseclient = baseclient

    async def get_all(  # noqa: A003
        self,
        installation_filter: str | None = None,
    ) -> List[Installation]:
        """List all Installation objects.

        Args:
            installation_filter: str

        Returns:
            all installations objects

        Optional filter (URL encoded JSON).
            * size: When the size filter is specified, when specified
            the matching Image metadata will be included in the response,
            if any. Possible values: SMALL|MEDIUM|ORIGINAL
            * gateways:
                gateway_model: openmotics|somfy|sense|healthbox3
            * openmotics:
                platform: CLASSIC|CORE|CORE_PLUS|ESAFE

        """
        path = "/base/installations"
        if installation_filter:
            query_params = {"filter": installation_filter}
            body = await self.baseclient.get(
                path=path,
                params=query_params,
            )
        else:
            body = await self.baseclient.get(path)

        return [
            Installation(**installation) for installation in body["data"]
        ]  # type: ignore

    async def get_by_id(
        self,
        installation_id: int,
    ) -> Installation:
        """Get a single Installation object.

        Args:
            installation_id: int

        Returns:
            a single Installation object

        """
        path = f"/base/installations/{installation_id}"
        body = await self.baseclient.get(path)
        installation = body["data"]

        return Installation(**installation)  # type: ignore
