"""Module containing the base of an light."""

from __future__ import annotations

from typing import TYPE_CHECKING, Any

from pydantic import parse_obj_as

from pyhaopenmotics.models.light import Light

if TYPE_CHECKING:
    from pyhaopenmotics.base import BaseClient  # pylint: disable=R0401


class OpenMoticsLights:  # noqa: SIM119
    """Object holding information of the OpenMotics lights.

    All actions related to lights or a specific light.
    """

    def __init__(self, baseclient: BaseClient) -> None:
        """Init the installations object.

        Args:
            baseclient: BaseClient
        """
        self.baseclient = baseclient

    async def get_all(  # noqa: A003
        self,
        installation_id: int,
        light_filter: str | None = None,
    ) -> list[Light]:
        """Get a list of all light objects.

        Args:
            installation_id: int
            light_filter: str

        Returns:
            Dict with all lights
        """
        path = f"/base/installations/{installation_id}/lights"

        if light_filter:
            query_params = {"filter": light_filter}
            body = await self.baseclient.get(
                path=path,
                params=query_params,
            )
        else:
            body = await self.baseclient.get(path)

        return parse_obj_as(list[Light], body["data"])

    async def get_by_id(
        self,
        installation_id: int,
        light_id: int,
    ) -> Light:
        """Get light by id.

        Args:
            installation_id: int
            light_id: int

        Returns:
            Returns a light with id
        """
        path = f"/base/installations/{installation_id}/lights/{light_id}"
        body = await self.baseclient.get(path)

        return Light.parse_obj(body["data"])

    async def toggle(
        self,
        installation_id: int,
        light_id: int,
    ) -> dict[str, Any]:
        """Toggle a specified light object.

        Args:
            installation_id: int
            light_id: int

        Returns:
            Returns a light with id
        """
        path = f"/base/installations/{installation_id}/lights/{light_id}/toggle"
        return await self.baseclient.post(path)

    async def turn_on(
        self,
        installation_id: int,
        light_id: int,
        value: int | None = 100,
    ) -> dict[str, Any]:
        """Turn on a specified light object.

        Args:
            installation_id: int
            light_id: int
            value: <0 - 100>

        Returns:
            Returns a light with id
        """
        if value is not None:
            value = min(value, 100)
            value = max(0, value)

        path = f"/base/installations/{installation_id}/lights/{light_id}/turn_on"
        payload = {"value": value}
        return await self.baseclient.post(path, json=payload)

    async def turn_off(
        self,
        installation_id: int,
        light_id: int | None = None,
    ) -> dict[str, Any]:
        """Turn off a specified light object.

        Args:
            installation_id: int
            light_id: int

        Returns:
            Returns a light with id
        """
        if light_id is None:
            # Turn off all lights
            path = f"/base/installations/{installation_id}/lights/turn_off"
        else:
            # Turn off light with id
            path = f"/base/installations/{installation_id}/lights/{light_id}/turn_off"
        return await self.baseclient.post(path)
