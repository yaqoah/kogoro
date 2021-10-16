from bot import PLAYERS_URL, LOGGER
import bot.proxy.team as sqwad
import bot.proxy as api
from bot.utils.interpret import image_to_base64, url_to_base64, base64_to_image


async def player_statistics(pid, lid=0):
    query = {
        "id": pid,
        "team": sqwad.tid,
        "season": api.season
    }
    data = (await api.link(PLAYERS_URL, query))[0]

    participate = dict()
    if not lid:
        for league in data["statistics"]:
            info = league["league"]
            if info["id"] is None or info["name"] is None:
                continue
            participate[info["id"]] = info["name"]

        return participate

    logoURL = url_to_base64(data["player"]["photo"])
    try:
        logoPIL = base64_to_image(logoURL)
        logoPIL.thumbnail((300, 300))
        logoURL = bytes(f"data:image/{logoPIL.format};base64,",
                        encoding="utf-8") + image_to_base64(logoPIL)
        interpretedURL = logoURL.decode("utf-8")
    except:
        LOGGER.info("resized image (api) unrecognized by pyrogram.")
    finally:
        interpretedURL = data["player"]["photo"]

    #  about: player
    name = data["player"]["name"]
    age = data["player"]["age"]
    nationality = data["player"]["nationality"]
    height = data["player"]["height"] \
        if data["player"]["height"] is not None else "N/A"
    injury = data["player"]["injured"] \
        if data["player"]["injured"] is not None else "N/A"
    stats = data["statistics"]
    #  stats: player
    appearances, minutes = 0, 0
    shots, on_target, goals, conceded, saves = 0, 0, 0, 0, 0
    passes, accuracy, key, assists = 0, 0, 0, 0
    tackles, blocks, interception, duels, won = 0, 0, 0, 0, 0
    dribbles_attempted, successful_dribbles = 0, 0
    fouls_drawn, fouls_commited = 0, 0
    yellow, red = 0, 0

    assemblage = list()
    if lid == 1999:
        for league in stats:
            assemblage.append(league)
    else:
        for tourn in stats:
            if tourn["league"]["id"] == lid:
                league = stats[stats.index(tourn)]
                assemblage.append(league)

    for league in assemblage:
        appearances += league["games"]["appearences"] \
            if league["games"]["appearences"] is not None else 0
        minutes += league["games"]["minutes"] \
            if league["games"]["minutes"] is not None else 0
        shots += league["shots"]["total"] \
            if league["shots"]["total"] is not None else 0
        on_target += league["shots"]["on"] \
            if league["shots"]["on"] is not None else 0
        goals += league["goals"]["total"] \
            if league["goals"]["total"] is not None else 0
        conceded += league["goals"]["conceded"] \
            if league["goals"]["conceded"] is not None else 0
        saves += league["goals"]["saves"] \
            if league["goals"]["saves"] is not None else 0
        passes += league["passes"]["total"] \
            if league["passes"]["total"] is not None else 0
        accuracy += league["passes"]["accuracy"] \
            if league["passes"]["accuracy"] is not None else 0
        key += league["passes"]["key"] \
            if league["passes"]["key"] is not None else 0
        assists += league["goals"]["assists"] \
            if league["goals"]["assists"] is not None else 0
        tackles += league["tackles"]["total"] \
            if league["tackles"]["total"] is not None else 0
        blocks += league["tackles"]["blocks"] \
            if league["tackles"]["blocks"] is not None else 0
        interception += league["tackles"]["interceptions"] \
            if league["tackles"]["interceptions"] is not None else 0
        duels += league["duels"]["total"] \
            if league["duels"]["total"] is not None else 0
        won += league["duels"]["won"] \
            if league["duels"]["won"] is not None else 0
        dribbles_attempted += league["dribbles"]["attempts"] \
            if league["dribbles"]["attempts"] is not None else 0
        successful_dribbles += league["dribbles"]["success"] \
            if league["dribbles"]["success"] is not None else 0
        fouls_drawn += league["fouls"]["drawn"] \
            if league["fouls"]["drawn"] is not None else 0
        fouls_commited += league["fouls"]["committed"] \
            if league["fouls"]["committed"] is not None else 0
        yellow += (league["cards"]["yellow"]
                   if league["cards"]["yellow"] is not None else 0) \
            + (league["cards"]["yellowred"]
                if league["cards"]["yellowred"] is not None else 0)
        red += (league["cards"]["red"]
                if league["cards"]["red"] is not None else 0) \
            + (league["cards"]["yellowred"]
                if league["cards"]["yellowred"] is not None else 0)

    return (
        [name, api.season, age, nationality, height, injury, appearances, minutes],
        [shots, on_target, goals, conceded, saves],
        [passes, accuracy, key, assists],
        [tackles, blocks, interception, duels, won],
        [dribbles_attempted, successful_dribbles],
        [fouls_drawn, fouls_commited, yellow, red],
        interpretedURL
    )
