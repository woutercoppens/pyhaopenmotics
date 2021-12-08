#!/usr/bin/env python3

"""
How to use this script:
    pip install python-dotenv
    export CLIENT_ID="dnfqsdfjqsjfqsdjfqf"
    export CLIENT_SECRET="djfqsdkfjqsdkfjqsdkfjqsdkfjkqsdjfkjdkfqjdskf"
    python cloud_example.py
"""


import asyncio

# UNCOMMENT THIS TO SEE ALL THE HTTPX INTERNAL LOGGING
import logging
import os

from dotenv import load_dotenv
from httpx import AsyncClient

from pyhaopenmotics import CloudClient

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
# username = os.environ['USERNAME']
# password = os.environ['PASSWORD']


async def main():
    async with CloudClient(
        client_id,
        client_secret,
    ) as bc:
        await bc.get_token()

    # user = await client.async_get_user()
    # print(user)

    installations = await bc.installations.get_all()
    print(installations)

    i_id = installations[0].id

    installation = await bc.installations.get_by_id(i_id)
    print(installation)
    print(installation.id)
    print(installation.name)

    outputs = await bc.outputs.get_all(i_id)
    print(outputs)

    print(outputs[0].state)

    # d_id = devices[0].id
    # m_id = devices[0].modules[0].id

    # await bc.async_set_minor_mode(d_id, m_id, SetpointMode.MANUAL, False)


# if __name__ == "__main__":
#     asyncio.run(main())

if __name__ == "__main__":
    loop = asyncio.get_event_loop()
    loop.run_until_complete(main())
