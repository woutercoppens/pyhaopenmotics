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
    async with CloudClient(
        client_id,
        client_secret,
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
