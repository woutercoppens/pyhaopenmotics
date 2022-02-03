#!/usr/bin/env python3
# noqa: E800
"""
Local Example.

How to use this script:
    pip install python-dotenv
    export LOCAL_HOST='192.168.0.2'
    export USERNAME="dnfqsdfjqsjfqsdjfqf"
    export PASSWORD="djfqsdkfjqsdkfjqsdkfjqsdkfjkqsdjfkjdkfqjdskf"
    python cloud_example.py
"""
import asyncio
import logging
import os

from dotenv import load_dotenv

from pyhaopenmotics import LocalGatewayClient

# UNCOMMENT THIS TO SEE ALL THE HTTPX INTERNAL LOGGING
log = logging.getLogger()
log.setLevel(logging.DEBUG)
log_format = logging.Formatter("[%(asctime)s] [%(levelname)s] - %(message)s")
console = logging.StreamHandler()
console.setLevel(logging.DEBUG)
console.setFormatter(log_format)
log.addHandler(console)

load_dotenv()

local_host = os.environ["LOCAL_HOST"]
username = os.environ["USER_NAME"]
password = os.environ["PASSWORD"]
port = os.environ["PORT"]
ssl = os.environ["SSL"]


async def main() -> None:
    """Show example on controlling your OpenMotics device."""
    async with LocalGatewayClient(
        host=local_host,
        username=username,
        password=password,
        port=port,
        ssl=ssl,
    ) as omclient:
        await omclient.get_token()

    installations = await omclient.installations.get_all()
    print(installations)

    i_id = installations[0].idx

    installation = await omclient.installations.get_by_id(i_id)
    print(installation)
    print(installation.idx)
    print(installation.name)

    outputs = await omclient.outputs.get_all(i_id)
    print(outputs)

    print(outputs[0].status.on)

    sensors = await omclient.sensors.get_all(i_id)
    print(sensors)


if __name__ == "__main__":
    asyncio.run(main())
