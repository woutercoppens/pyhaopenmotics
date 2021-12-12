"""Module containing the base of an output."""
from __future__ import annotations

import json
from typing import TYPE_CHECKING, Any, List

from pyhaopenmotics.models.shutter import Shutter

if TYPE_CHECKING:
    from pyhaopenmotics.base import BaseClient  # pylint: disable=R0401


class ShuttersCtrl:  # noqa: SIM119
    """Object holding information of the OpenMotics outputs.

    All actions related to Outputs or a specific Output.
    """

    def __init__(self, baseclient: BaseClient) -> None:
        """Init the installations object.

        Args:
            baseclient: BaseClient
        """
        self.baseclient = baseclient

    async def get_all(  # type: ignore
        self,
        installation_id: int,
        shutter_filter: str | None = None,
    ) -> List[Shutter]:
        """List all Shutter objects.

        Args:
            installation_id: int
            shutter_filter: Optional filter

        Returns:
            Dict with all shutters

        usage: The usage filter allows the Shutters to be filtered for their
            intended usage.
            CONTROL: These Shutters can be controlled directly and are not
                managed by an internal process.
        """
        path = f"/base/installations/{installation_id}/shutters"
        if shutter_filter:
            query_params = {"filter": shutter_filter}
            body = await self.baseclient.get(
                path=path,
                params=query_params,
            )
        else:
            body = await self.baseclient.get(path)

        return [Shutter(**shutter) for shutter in body["data"]]  # type: ignore

    async def get_by_id(  # type: ignore
        self,
        installation_id: int,
        shutter_id: int,
    ) -> Shutter:
        """Get a specified Shutter object.

        Args:
            installation_id: int
            shutter_id: int

        Returns:
            Returns a shutter with id
        """
        path = f"/base/installations/{installation_id}/shutters/{shutter_id}"
        body = await self.baseclient.get(path)
        shutter = body["data"]

        return Shutter(**shutter)  # type: ignore

    async def move_up(
        self,
        installation_id: int,
        shutter_id: int,
    ) -> dict[str, Any]:
        """Move the specified Shutter into the upwards position.

        Args:
            installation_id: int
            shutter_id: int

        Returns:
            Returns a shutter with id
        """
        path = f"/base/installations/{installation_id}/shutters/{shutter_id}/up"
        return await self.baseclient.post(path)

    async def move_down(
        self,
        installation_id: int,
        shutter_id: int,
    ) -> dict[str, Any]:
        """Move the specified Shutter into the downwards position.

        Args:
            installation_id: int
            shutter_id: int

        Returns:
            Returns a shutter with id
        """
        path = f"/base/installations/{installation_id}/shutters/{shutter_id}/down"
        return await self.baseclient.post(path)

    async def stop(
        self,
        installation_id: int,
        shutter_id: int,
    ) -> dict[str, Any]:
        """Stop any movement of the specified Shutter.

        Args:
            installation_id: int
            shutter_id: int

        Returns:
            Returns a shutter with id
        """
        path = f"/base/installations/{installation_id}/shutters/{shutter_id}/stop"
        return await self.baseclient.post(path)

    async def change_position(
        self,
        installation_id: int,
        shutter_id: int,
        position: int,
    ) -> dict[str, Any]:
        """Change the position of the specified Shutter.

        The position can be set from 0 to steps (excluded). The steps value can be
        found in the configuration field of a Shutter.
        Not all gateways or shutters support this feature.

        Args:
            installation_id: int
            shutter_id: int
            position: int  (in body)

        Returns:
            Returns a shutter with id
        """
        # E501 line too long
        path = (
            f"/base/installations/{installation_id}"
            f"/shutters/{shutter_id}/change_position"
        )
        payload = json.dumps(
            {
                "position": position,
            }
        )
        return await self.baseclient.post(path, json=payload)

    async def change_relative_position(
        self,
        installation_id: int,
        shutter_id: int,
        offset: int,
    ) -> dict[str, Any]:
        """Change the relative position of the specified Shutter.

        The offset can be set from -steps (excluded) to steps (excluded).
        The steps value can be found in the configuration field of a Shutter.
        Not all gateways or shutters support this feature.

        Args:
            installation_id: int
            shutter_id: int
            offset: int (in body)

        Returns:
            Returns a shutter with id
        """
        # E501 line too long
        path = (
            f"/base/installations/{installation_id}"
            f"/shutters/{shutter_id}/change_relative_position"
        )
        payload = json.dumps(
            {
                "offset": offset,
            }
        )
        return await self.baseclient.post(path, json=payload)

    async def lock(
        self,
        installation_id: int,
        shutter_id: int,
    ) -> dict[str, Any]:
        """Lock the specified Shutter to prevent future movements.

        The behavior is depending of the capabilities of the Shutter:
            LOCAL_LOCK capability: this lock is a hardware lock, without manual
            override through a local interface.
            CLOUD_LOCK capability: this lock is a software lock in the cloud,
            thus you can still move the shutter through a local interface.


        Args:
            installation_id: int
            shutter_id: int

        Returns:
            Returns the lock_type as response.
        """
        path = f"/base/installations/{installation_id}/shutters/{shutter_id}/lock"
        return await self.baseclient.post(path)

    async def unlock(
        self,
        installation_id: int,
        shutter_id: int,
    ) -> dict[str, Any]:
        """Undo the lock action of the specified Shutter.

        Args:
            installation_id: int
            shutter_id: int

        Returns:
            Returns a shutter with id
        """
        path = f"/base/installations/{installation_id}/shutters/{shutter_id}/unlock"
        return await self.baseclient.post(path)

    async def preset(
        self,
        installation_id: int,
        shutter_id: int,
        position: int,
    ) -> dict[str, Any]:
        """Change the preset position of the specified Shutter.

        The position can be set from 0 to steps (excluded). The steps value can be
        found in the configuration field of a Shutter.
        Not all gateways or shutters support this feature.

        Args:
            installation_id: int
            shutter_id: int
            position: int (in body)

        Returns:
            Returns a shutter with id
        """
        path = f"/base/installations/{installation_id}/shutters/{shutter_id}/preset"
        payload = json.dumps(
            {
                "position": position,
            }
        )
        return await self.baseclient.post(path, json=payload)

    async def move_to_preset(
        self,
        installation_id: int,
        shutter_id: int,
    ) -> dict[str, Any]:
        """Move the specified Shutter to its preset position (defined in POST .../preset).

        Not all gateways or shutters support this feature.

        Args:
            installation_id: int
            shutter_id: int

        Returns:
            Returns a shutter with id
        """
        path = f"/base/installations/{installation_id}/shutters/{shutter_id}/move"
        return await self.baseclient.post(path)
