"""Output Model for the OpenMotics API."""
from __future__ import annotations

from typing import Optional

from pydantic import BaseModel, Field


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

    id: int  # noqa:A003
    name: Optional[str] = None
    actions: Optional[dict] = None
    location: Optional[dict] = None
    version: Optional[str] = Field(None, alias="_version")

    def __str__(self):
        """Represent the class objects as a string.

        Returns:
            string

        """
        return f"{self.id}_{self.name}"
