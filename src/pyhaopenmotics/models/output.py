"""Output Model for the OpenMotics API."""
from __future__ import annotations

from typing import List, Optional

from pydantic import BaseModel, Field


class Output(BaseModel):
    """Class holding an OpenMotics Output.

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

    # pylint: disable=too-many-instance-attributes
    id: int  # noqa:A003
    name: Optional[str] = None
    output_type: str = Field(None, alias="type")
    capabilities: Optional[List] = None
    location: Optional[dict] = None
    installation_id: Optional[int] = None
    gateway_id: Optional[int] = None
    floor_id: Optional[int] = None
    room_id: Optional[int] = None
    metadata: Optional[dict] = None
    status: Optional[dict] = None
    last_state_change: Optional[float] = None
    version: Optional[str] = Field(None, alias="_version")

    _brightness: Optional[int] = None

    def __str__(self):
        """Represent the class objects as a string.

        Returns:
            string

        """
        return f"{self.id}_{self.name}_{self.output_type}"

    @property
    def state(self):
        """Return the state of the output.

        Returns:
            state
        """
        return self.status["on"]

    @property
    def brightness(self):
        """Return the brightness of the output.

        Returns:
            brightness
        """
        try:
            self._brightness = self.status["value"]
        except KeyError:
            self._brightness = None
        return self._brightness
