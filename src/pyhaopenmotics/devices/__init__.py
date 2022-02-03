"""Directory holding devices."""
from pyhaopenmotics.devices.groupactions import OpenMoticsGroupActions
from pyhaopenmotics.devices.installations import OpenMoticsInstallations
from pyhaopenmotics.devices.lights import OpenMoticsLights
from pyhaopenmotics.devices.outputs import OpenMoticsOutputs
from pyhaopenmotics.devices.sensors import OpenMoticsSensors
from pyhaopenmotics.devices.shutters import OpenMoticsShutters

__all__ = [
    "OpenMoticsInstallations",
    "OpenMoticsOutputs",
    "OpenMoticsGroupActions",
    "OpenMoticsShutters",
    "OpenMoticsLights",
    "OpenMoticsSensors",
]
