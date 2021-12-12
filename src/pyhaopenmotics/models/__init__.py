"""Init file for the models."""
from pyhaopenmotics.models.groupaction import GroupAction
from pyhaopenmotics.models.installation import Installation
from pyhaopenmotics.models.output import Output
from pyhaopenmotics.models.shutter import Shutter

__all__ = [
    "Installation",
    "GroupAction",
    "Output",
    "Shutter",
]
