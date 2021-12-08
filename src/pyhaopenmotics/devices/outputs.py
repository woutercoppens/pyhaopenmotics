""" Module containing the base of an output."""

from __future__ import annotations

from typing import TYPE_CHECKING, Any

from cached_property import cached_property

from ..models.output import Output

if TYPE_CHECKING:
    from .base import BaseClient  # pylint: disable=R0401


class OutputsCtrl:
    """Object holding information of the OpenMotics outputs.

    All actions related to Outputs or a specific Output.
    """

    def __init__(self, baseclient: BaseClient):
        """Init the installations object.

        Args:
            baseclient: BaseClient
        """
        self.baseclient = baseclient

    async def get_all(  # noqa: A003
        self,
        installation_id: int,
        output_filter: str | None = None,
    ) -> dict[str, Any]:
        """Get a list of all output objects.

        Args:
            installation_id: int

        Returns:
            Dict with all outputs
        """
        path = f"/base/installations/{installation_id}/outputs"

        if output_filter:
            query_params = {"filter": output_filter}
            body = await self.baseclient._get(
                path=path,
                params=query_params,
            )
        else:
            body = await self.baseclient._get(path)

        return [Output(**output) for output in body["data"]]

    async def get_by_id(
        self,
        installation_id: int,
        output_id: int,
    ) -> Output:
        """Get output by id.

        Args:
            installation_id: int
            output_id: int

        Returns:
            Returns a output with id
        """
        path = f"/base/installations/{installation_id}/outputs/{output_id}"
        body = await self.baseclient._get(path)
        output = body["data"]

        return Ouput(**output)

    async def toggle(
        self,
        installation_id: int,
        output_id: int,
    ) -> dict[str, Any]:
        """Toggle a specified Output object.

        Args:
            installation_id: int
            output_id: int

        Returns:
            Returns a output with id
        """
        path = f"/base/installations/{installation_id}/outputs/{output_id}/toggle"
        return await self.baseclient._post(path)

    async def turn_on(
        self,
        installation_id: int,
        output_id: int,
        value: int | None = 100,
    ) -> dict[str, Any]:
        """Turn on a specified Output object.

        Args:
            installation_id: int
            output_id: int
            value: <0 - 100>

        Returns:
            Returns a output with id
        """
        if value > 100:
            value = 100

        path = f"/base/installations/{installation_id}/outputs/{output_id}/turn_on"
        payload = {"value": value}
        return await self.baseclient._post(path, json=payload)

    async def turn_off(
        self,
        installation_id: int,
        output_id: int | None = None,
    ) -> dict[str, Any]:
        """Turn off a specified Output object.

        Args:
            installation_id: int
            output_id: int

        Returns:
            Returns a output with id
        """
        if output_id is None:
            # Turn off all lights
            path = f"/base/installations/{installation_id}/outputs/turn_off"
        else:
            # Turn off light with id
            path = f"/base/installations/{installation_id}/outputs/{output_id}/turn_off"
        return await self.baseclient._post(path)
