"""Installation Model for the OpenMotics API."""
from __future__ import annotations

from abc import ABC
from dataclasses import dataclass
from enum import auto
from typing import Any, List, Optional, Union

from pydantic import BaseModel, Field, validator

from .util import StrEnum


class Installation(BaseModel):
    """Object holding an OpenMotics Installation.

    # noqa: E800
    # {
    #     'id': 1,
    #     'name': 'John Doe',
    #     'description': '',
    #     'gateway_model': 'openmotics',
    #     '_acl': {'configure': {'allowed': True}, 'view': {'allowed': True},
    #             'control': {'allowed': True}},
    #     '_version': 1.0, 'user_role': {'role': 'ADMIN', 'user_id': 1},
    #     'registration_key': 'xxxxx-xxxxx-xxxxxxx',
    #     'platform': 'CLASSIC',
    #     'building_roles': [],
    #     'version': '1.16.5',
    #     'network': {'local_ip_address': '172.16.1.25'},
    #     'flags': {'UNREAD_NOTIFICATIONS': 0, 'ONLINE': None},
    #     'features':
    #         {'outputs': {'available': True, 'used': True, 'metadata': None},
    #          'thermostats': {'available': True, 'used': False, 'metadata': None},
    #          'energy': {'available': True, 'used': True, 'metadata': None},
    #          'apps': {'available': True, 'used': False, 'metadata': None},
    #          'shutters': {'available': True, 'used': False, 'metadata': None},
    #          'consumption': {'available': False, 'used': False, 'metadata': None},
    #          'scheduler': {'available': True, 'used': True, 'metadata': None},
    #          'ems': {'available': False, 'used': False, 'metadata': None}},
    #          'gateway_features': ['metrics', 'dirty_flag', 'scheduling',
    #          'factory_reset', 'isolated_plugins',
    #          'websocket_maintenance', 'shutter_positions',
    #          'ventilation', 'default_timer_disabled',
    #          '100_steps_dimmer', 'input_states']
    # }
    """

    # installation_id: Union[int,str] = Field(..., alias="id")
    id: Optional[int] = None
    name: Optional[str] = None
    description: Optional[str] = None
    gateway_model: Optional[str] = None
    acl: Optional[dict] = Field(None, alias="_acl")
    version: Optional[str] = Field(None, alias="_version")
    user_role: Optional[dict] = None
    registration_key: Optional[str] = None
    platform: Optional[str] = None
    building_roles: Optional[dict] = None
    network: Optional[dict] = None
    flags: Optional[dict] = None
    features: Optional[dict] = None

    def __eq__(self, other: Installation):
        if not isinstance(other, Installation):
            return False

        return (
            # self.installation_id == other.installation_id
            self.id == other.id
            and self.name == other.name
            and self.description == other.description
            and self.acl == other.acl
            and self.version == other.version
            and self.user_role == other.user_role
            and self.registration_key == other.registration_key
            and self.platform == other.platform
            and self.building_roles == other.building_roles
            and self.network == other.network
            and self.flags == other.flags
            and self.features == other.features
        )

    def __str__(self):
        return f"{self.id}_{self.name}"
