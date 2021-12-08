""" Module containing the base of an output."""

from __future__ import annotations

from typing import TYPE_CHECKING, Any

from cached_property import cached_property

from ..models.groupaction import GroupAction

if TYPE_CHECKING:
    from .base import BaseClient  # pylint: disable=R0401


class GroupActionsCtrl:
    """Object holding information of the OpenMotics groupactions.

    All actions related to groupaction or a specific groupaction.
    """

    def __init__(self, baseclient: BaseClient):
        """Init the installations object.

        Args:
            baseclient: BaseClient
        """
        self.baseclient = baseclient

    async def get_all(
        self,
        installation_id: int,
        groupactions_filter: str | None = None,
    ) -> dict[str, Any]:
        """Call lists all GroupAction objects.

        Args:
            installation_id: int
            groupactions_filter: Optional filter

        Returns:
            Dict with all groupactions

        usage: The usage filter allows the GroupActions to be filtered for
            their intended usage.
            SCENE: These GroupActions can be considered a scene,
                e.g. watching tv or romantic dinner.
        # noqa: E800
        # [{
        #      "_version": <version>,
        #      "actions": [
        #          <action type>, <action number>,
        #          <action type>, <action number>,
        #          ...
        #      ],
        #  "id": <id>,
        #  "location": {
        #      "installation_id": <installation id>
        #  },
        #  "name": "<name>"
        #  }
        """
        path = f"/base/installations/{installation_id}/groupactions"
        if groupactions_filter:
            query_params = {"filter": groupactions_filter}
            body = await self.baseclient._get(
                path=path,
                params=query_params,
            )
        else:
            body = await self.baseclient._get(path)

        return [GroupAction(**grpctn) for grpctn in body["data"]]

    async def get_by_id(
        self,
        installation_id: int,
        groupaction_id: int,
    ) -> dict[str, Any]:
        """Get a specified groupaction object.

        Args:
            installation_id: int
            groupaction_id: int

        Returns:
            Returns a groupaction with id
        """
        path = f"/base/installations/{installation_id}/groupactions/{groupaction_id}"
        body = await self.baseclient._get(path)
        output = body["data"]

        return Ouput(**output)

    async def trigger(
        self,
        installation_id: int,
        groupaction_id: int,
    ) -> dict[str, Any]:
        """Trigger a specified groupaction object.

        Args:
            installation_id: int
            groupaction_id: int

        Returns:
            Returns a groupaction with id
        """
        # E501 line too long
        path = (
            f"/base/installations/{installation_id}"
            f"/groupactions/{groupaction_id}/trigger"
        )
        return await self.baseclient._post(path)

    async def by_usage(
        self,
        installation_id: int,
        groupaction_usage: str,
    ) -> dict[str, Any]:
        """Return a specified groupaction object.

        The usage filter allows the GroupActions to be filtered for their
        intended usage.

        Args:
            installation_id: int
            groupaction_usage: str

        Returns:
            Returns a groupaction with id
        """
        path = f"/base/installations/{installation_id}/groupactions"
        query_params = {"usage": groupaction_usage.upper()}
        return await self.baseclient._get(path, params=query_params)

    async def scenes(self, installation_id: int) -> dict[str, Any]:
        """Return all scenes object.

        SCENE: These GroupActions can be considered a scene,
            e.g. watching tv or romantic dinner.

        Args:
            installation_id: int

        Returns:
            Returns all scenes
        """
        return await self.by_usage(installation_id, "SCENE")
