"""Output Model for the OpenMotics API."""
from __future__ import annotations

from abc import ABC
from dataclasses import dataclass
from enum import auto
from typing import Any, List, Optional, Union

from pydantic import BaseModel, Field, validator

from .util import StrEnum


class Output(BaseModel):
    """Object holding an OpenMotics Output.

    # noqa: E800
     # [{
     #     'name': 'name1',
     #     'type': 'OUTLET',
     #     'capabilities': ['ON_OFF'],
     #     'location': {'floor_coordinates': {'x': None, 'y': None},
     #     'installation_id': 21,
     #     'gateway_id': 408,
     #     'floor_id': None,
     #     'room_id': None},
     #     'metadata': None,
     #     'status': {'on': False, 'locked': False, 'manual_override': False},
     #     'last_state_change': 1633099611.275243,
     #     'id': 18,
     #     '_version': 1.0
     #     },{
     #     'name': 'name2',
     #     'type': 'OUTLET',
     #     ...
    """

    id: int
    name: str
    output_type: str = Field(None, alias="type")
    capabilities: List = None
    location: Optional[dict] = None
    installation_id: Optional[int] = None
    gateway_id: Optional[int] = None
    floor_id: Optional[int] = None
    room_id: Optional[int] = None
    metadata: Optional[dict] = None
    status: dict
    last_state_change: Optional[float] = None
    version: Optional[str] = Field(None, alias="_version")

    def __eq__(self, other: Output):
        if not isinstance(other, Output):
            return False

        return (
            # self.installation_id == other.installation_id
            self.id == other.id
            and self.name == other.name
            and self.output_type == other.output_type
            and self.capabilities == other.capabilities
            and self.location == other.location
            and self.installation_id == other.installation_id
            and self.gateway_id == other.gateway_id
            and self.floor_id == other.floor_id
            and self.metadata == other.metadata
            and self.status == other.status
            and self.last_state_change == other.last_state_change
            and self.version == other.version
        )

    def __str__(self):
        return f"{self.id}_{self.name}_{self.output_type}"

    @property
    def state(self):
        if self.status["on"] is True:
            return True
        else:
            return False

    @property
    def brightness(self):
        try:
            self._brightness = self.status["value"]
        except KeyError:
            self._brightness = None
        return self._brightness


class Status(BaseModel):
    """Object holding the status of an Output.

    'status': {'on': False, 'locked': False, 'manual_override': False},
    """

    on: bool
    locked: bool
    manual_override: bool
