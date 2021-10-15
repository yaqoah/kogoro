from bot.session import mysession
season = int()


async def link(uri, query):
    async with mysession as sesh:
        return await sesh.fetch(uri, query)

from.team import tid, name
