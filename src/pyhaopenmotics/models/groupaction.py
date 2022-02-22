"""Output Model for the OpenMotics API."""
from __future__ import annotations

from typing import List, Optional

from pydantic import BaseModel, Field


class FloorCoordinates(BaseModel):
    """Class holding the floor_coordinates."""

    x: Optional[int] = None
    y: Optional[int] = None


class Location(BaseModel):
    """Class holding the location."""

    floor_coordinates: Optional[FloorCoordinates] = None
    floor_id: Optional[int] = None
    installation_id: Optional[int] = None
    room_id: Optional[int] = None


class GroupAction(BaseModel):
    """Object holding an OpenMotics GroupAction.

    # noqa: E800
    # {
    # "_version": <version>,
    # "actions": [
    #     <action type>, <action number>,
    #     <action type>, <action number>,
    #     ...
    # ],
    # "id": <id>,
    # "location": {
    #     "installation_id": <installation id>
    # },
    # "name": "<name>"
    # }
    """

    idx: int = Field(..., alias="id")
    local_id: int
    name: Optional[str] = None
    actions: Optional[List] = None
    location: Optional[Location] = None
    version: Optional[str] = Field(None, alias="_version")

    def __str__(self):
        """Represent the class objects as a string.

        Returns:
            string

        """
        return f"{self.idx}_{self.name}"
