import aiohttp
import asyncio
import traceback
import sys
from bot import (RAPID_API_KEY_REQ, RAPID_API_HOST_REQ,
                 RAPID_API_KEY_VALUE, RAPID_API_HOST_VALUE, LOGGER)

HEADERS = {
    RAPID_API_HOST_REQ: RAPID_API_HOST_VALUE,
    RAPID_API_KEY_REQ: RAPID_API_KEY_VALUE
}


class Session:
    async def __aenter__(self):
        self.session = aiohttp.ClientSession(headers=HEADERS)
        return self

    async def __aexit__(self, exc_type, exc_val, exc_tb):
        await self.session.close()
        self.session = None

    async def fetch(self, URL, params):
        try:
            async with self.session.get(url=URL, params=params) as result:
                to_url = URL \
                         + f"?{list(params.keys())[0]}=" \
                           f"{'+'.join(str(params[list(params.keys())[0]]).split(' '))}" \
                         + "".join([f"&{key}="
                                    f"{'+'.join(str(params[key]).split(' '))}"
                                    for key in list(params.keys())[1:] if key])
                assert str(result.url) == to_url
                return (await result.json())["response"]
        except aiohttp.ClientConnectorError as conn:
            LOGGER.warning("http error: connection failed to Football-Api. exiting.")
            traceback.print_exc()
            sys.exit()


mysession = Session()
