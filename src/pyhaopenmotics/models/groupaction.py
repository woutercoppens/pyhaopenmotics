"""Output Model for the OpenMotics API."""
from __future__ import annotations

from abc import ABC
from dataclasses import dataclass
from enum import auto
from typing import Any, List, Optional, Union

from pydantic import BaseModel, Field, validator

from .util import StrEnum


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

    id: int
    name: str
    actions: Optional[dict] = None
    location: Optional[dict] = None
    version: Optional[str] = Field(None, alias="_version")

    def __eq__(self, other: Shutter):
        if not isinstance(other, Shutter):
            return False

        return (
            # self.installation_id == other.installation_id
            self.id == other.id
            and self.name == other.name
            and self.actions == other.actions
            and self.location == other.location
            and self.version == other.version
        )

    def __str__(self):
        return f"{self.id}_{self.name}"
