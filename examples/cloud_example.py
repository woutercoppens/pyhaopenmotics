#!/usr/bin/env python3
# noqa: E800

"""
Cloud example.

How to use this script:
    pip install python-dotenv
    export CLIENT_ID="dnfqsdfjqsjfqsdjfqf"
    export CLIENT_SECRET="djfqsdkfjqsdkfjqsdkfjqsdkfjkqsdjfkjdkfqjdskf"
    python cloud_example.py
"""
import asyncio
import logging
import os

from dotenv import load_dotenv

from pyhaopenmotics import CloudClient

# UNCOMMENT THIS TO SEE ALL THE HTTPX INTERNAL LOGGING
log = logging.getLogger()
log.setLevel(logging.DEBUG)
log_format = logging.Formatter("[%(asctime)s] [%(levelname)s] - %(message)s")
console = logging.StreamHandler()
console.setLevel(logging.DEBUG)
console.setFormatter(log_format)
log.addHandler(console)


load_dotenv()

client_id = os.environ["CLIENT_ID"]
client_secret = os.environ["CLIENT_SECRET"]


async def main():
    """Show example on controlling your OpenMotics device."""
    async with CloudClient(
        client_id,
        client_secret,
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

    print(outputs[0])

    sensors = await omclient.sensors.get_all(i_id)
    print(sensors)

    ga = await omclient.groupactions.get_all(i_id)
    print(ga)

    tg = await omclient.thermostats.groups.get_all(i_id)
    print(tg)

    tu = await omclient.thermostats.units.get_all(i_id)
    print(tu)

    shu = await omclient.shutters.get_all(i_id)
    print(shu)

    await omclient.close()


if __name__ == "__main__":
    asyncio.run(main())
