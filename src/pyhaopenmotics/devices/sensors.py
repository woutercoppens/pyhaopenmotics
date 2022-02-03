"""Module containing the base of an sensor."""

from __future__ import annotations

from typing import TYPE_CHECKING, Any

from pydantic import parse_obj_as

from pyhaopenmotics.models.sensor import Sensor

if TYPE_CHECKING:
    from pyhaopenmotics.base import BaseClient  # pylint: disable=R0401


class OpenMoticsSensors:  # noqa: SIM119
    """Object holding information of the OpenMotics sensors.

    All actions related to Sensors or a specific Sensor.
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
        sensor_filter: str | None = None,
    ) -> list[Sensor]:
        """Get a list of all sensor objects.

        Args:
            installation_id: int
            sensor_filter: str

        Returns:
            Dict with all sensors
        """
        path = f"/base/installations/{installation_id}/sensors"

        if sensor_filter:
            query_params = {"filter": sensor_filter}
            body = await self.baseclient.get(
                path=path,
                params=query_params,
            )
        else:
            body = await self.baseclient.get(path)

        # return [sensor(**sensor) for sensor in body["data"]]  # type: ignore
        return parse_obj_as(list[Sensor], body["data"])

    async def get_by_id(
        self,
        installation_id: int,
        sensor_id: int,
    ) -> Sensor:
        """Get sensor by id.

        Args:
            installation_id: int
            sensor_id: int

        Returns:
            Returns a sensor with id
        """
        path = f"/base/installations/{installation_id}/sensors/{sensor_id}"
        body = await self.baseclient.get(path)
        # sensor = body["data"]

        return Sensor.parse_obj(body["data"])
