from bot import (TEAMS_URL, FIXTURES_URL, TEAM_STATS_URL,
                 LEAGUES_URL, PLAYERS_URL, LOGGER)
import bot.proxy as api
from bot.utils.interpret import (image_to_base64, url_to_base64,
                                 base64_to_image)

tid = int()
name = str()


async def compete(team):
    global tid, name

    query = {
        "name": team
    }

    info = await api.link(TEAMS_URL, query)

    if info:
        name = info[0]["team"]["name"]
        tid = info[0]["team"]["id"]
        return True

    return False


async def next_ten():
    query = {
        "season": api.season,
        "team": tid,
        "next": 10
    }
    fixtures = await api.link(FIXTURES_URL, query)

    if not fixtures:
        any_query = {
            "season": api.season,
            "team": tid,
        }

        fixtures = await api.link(FIXTURES_URL, any_query)

    upcoming = dict()
    for match in fixtures:
        for side in match["teams"]:
            if match["teams"][side]["id"] == tid:
                continue
            upcoming[match["fixture"]["id"]] = match["teams"][side]["name"]

    return upcoming


async def all_leagues():
    query = {
        "season": api.season,
        "team": tid
    }
    leagues = await api.link(LEAGUES_URL, query)

    return {k["league"]["id"]: k["league"]["name"] for k in leagues}


async def team_statistics(lid: int) -> tuple:
    query = {
        "league": lid,
        "season": api.season,
        "team": tid
    }
    team = await api.link(TEAM_STATS_URL, query)

    logoURL = url_to_base64(team["team"]["logo"])
    try:
        logoPIL = base64_to_image(logoURL)
        logoPIL.thumbnail((300, 300))
        logoURL = bytes(f"data:image/{logoPIL.format};base64,",
                        encoding="utf-8") + image_to_base64(logoPIL)
        interpretedURL = logoURL.decode("utf-8")
    except:
        LOGGER.info("resized image (api) unrecognized by pyrogram.")
    finally:
        interpretedURL = team["team"]["logo"]

    minutes = team["goals"]["for"]["minute"]
    goals = 0
    peaked = "-"
    for scope in minutes:
        bracket = minutes[scope]["total"]
        total = 0 if bracket is None else int(bracket)
        if total > goals:
            goals = bracket
            peaked = scope

    minutes = team["goals"]["against"]["minute"]
    goals = 0
    nadired = "-"
    for scope in minutes:
        bracket = minutes[scope]["total"]
        total = 0 if bracket is None else int(bracket)
        if total > goals:
            goals = total
            nadired = scope

    return (
        interpretedURL, team["team"]["name"], team["form"],
        [
            team["fixtures"]["wins"]["total"],
            team["fixtures"]["draws"]["total"],
            team["fixtures"]["loses"]["total"]
        ],
        team["goals"]["for"]["total"]["total"], peaked,
        team["goals"]["against"]["total"]["total"], nadired,
        team["biggest"]["streak"]["loses"],
        team["failed_to_score"]["total"],
        team["biggest"]["streak"]["wins"],
        team["clean_sheet"]["total"]
    )


async def all_players():
    query = {
        "team": tid,
        "season": api.season
    }

    playersJSON = await api.link(PLAYERS_URL, query)

    players = dict()
    for player in playersJSON:
        pid = player["player"]["id"]
        pname = player["player"]["name"]
        players[pid] = pname

    return players
