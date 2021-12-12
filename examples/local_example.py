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
username = os.environ["USERNAME"]
password = os.environ["PASSWORD"]


async def main():
    async with LocalGatewayClient(
        host=local_host,
        username=username,
        password=password,
    ) as client:
        await client.get_token()

    # user = await client.async_get_user()
    # print(user)

    installations = await client.installations.get_all()
    print(installations)

    i_id = installations[0].id

    installation = await client.installations.get_by_id(i_id)
    print(installation)
    print(installation.id)
    print(installation.name)

    outputs = await client.outputs.get_all(i_id)
    print(outputs)

    print(outputs[0].state)


if __name__ == "__main__":
    loop = asyncio.get_event_loop()
    loop.run_until_complete(main())
