"""Output Model for the OpenMotics API."""
from __future__ import annotations

from abc import ABC
from dataclasses import dataclass
from enum import auto
from typing import Any, List, Optional, Union

from pydantic import BaseModel, Field, validator

from .util import StrEnum


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
    # "capabilities": ["UP_DOWN", "POSITION", "RELATIVE_POSITION", "HW_LOCK"|"CLOUD_LOCK", "PRESET", "CHANGE_PRESET"],
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

    id: int
    name: str
    configuration: Optional[dict] = None
    location: Optional[dict] = None
    capabilities: Optional[int] = None
    status: dict
    version: Optional[str] = Field(None, alias="_version")

    def __eq__(self, other: Shutter):
        if not isinstance(other, Shutter):
            return False

        return (
            # self.installation_id == other.installation_id
            self.id == other.id
            and self.name == other.name
            and self.configuration == other.configuration
            and self.capabilities == other.capabilities
            and self.location == other.location
            and self.status == other.status
            and self.version == other.version
        )

    def __str__(self):
        return f"{self.id}_{self.name}"

    @property
    def state(self):
        try:
            self._state = self.status["state"]
        except KeyError:
            self._state = None
        return self._state

    @property
    def position(self):
        try:
            self._position = self.status["position"]
        except KeyError:
            self._position = None
        return self._position
