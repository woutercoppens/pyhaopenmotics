"""Output Model for the OpenMotics API."""
from __future__ import annotations

from typing import Optional

from pydantic import BaseModel, Field


class Shutter(BaseModel):
    """Object holding an OpenMotics Shutter.

    # noqa: E800
    # {
    # "_version": <version>,
    # "configuration": {
    #     "group_1": null | <group id>,
    #     "group_2": null | <group id>,
    #     "name": "<name>",
    #     "steps": null | <number of steps>,
    #     "timer_down": <timer down>,
    #     "timer_up": <timer up>,
    #     "up_down_config": <up down configuration>
    # },
    # "id": <id>,
    # "capabilities": ["UP_DOWN", "POSITION", "RELATIVE_POSITION",
    #          "HW_LOCK"|"CLOUD_LOCK", "PRESET", "CHANGE_PRESET"],
    # "location": {
    #     "floor_coordinates": {
    #         "x": null | <x coordinate>,
    #         "y": null | <y coordinate>
    #     },
    #     "floor_id": null | <floor id>,
    #     "installation_id": <installation id>,
    #     "room_id": null | <room_id>
    # },
    # "name": "<name>",
    # "status": {
    #     "last_change": <epoch in seconds>
    #     "position": null | <position>,
    #     "state": null | "UP|DOWN|STOP|GOING_UP|GOING_DOWN",
    #     "locked": true | false,
    #     "manual_override": true | false
    # }
    # }
    """

    # pylint: disable=too-many-instance-attributes
    id: int  # noqa:A003
    name: Optional[str] = None
    configuration: Optional[dict] = None
    location: Optional[dict] = None
    capabilities: Optional[int] = None
    status: Optional[dict] = None
    version: Optional[str] = Field(None, alias="_version")

    _state: Optional[bool] = None
    _position: Optional[str] = None

    def __str__(self):
        """Represent the class objects as a string.

        Returns:
            string

        """
        return f"{self.id}_{self.name}"

    @property
    def state(self):
        """Return state of a shutter.

        Returns:
            bool
        """
        try:
            self._state = self.status["state"]
        except KeyError:
            self._state = None
        return self._state

    @property
    def position(self):
        """Return position of a shutter.

        Returns:
            position
        """
        try:
            self._position = self.status["position"]
        except KeyError:
            self._position = None
        return self._position
