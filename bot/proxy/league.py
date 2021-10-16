from bot import TOP_SCORERS_URL, TOP_ASSISTS_URL, TOP_RED_CARDS_URL, TOP_YELLOW_CARDS_URL
import bot.proxy as api


async def league_statistics(lid: int) -> tuple:
    urls = [TOP_SCORERS_URL, TOP_ASSISTS_URL, TOP_RED_CARDS_URL, TOP_YELLOW_CARDS_URL]
    scorers = list()
    assistants = list()
    reds = list()
    yellows = list()

    query = {
        "league": lid,
        "season": api.season
    }
    for page in urls:
        top_data = (await api.link(page, query))[:3]
        for player in top_data:
            first = player["player"]["firstname"]
            second = player["player"]["lastname"]
            alias = player["statistics"][0]["team"]["name"]

            name = first + " " + second
            team = alias if alias is not None else "N/A"
            if page == TOP_SCORERS_URL:
                total = player["statistics"][0]["goals"]["total"]
                goals = total if total is not None else 0
                scorers.append((team, name, goals))
            elif page == TOP_ASSISTS_URL:
                total = player["statistics"][0]["goals"]["assists"]
                assists = total if total is not None else 0
                assistants.append((team, name, assists))
            elif page == TOP_RED_CARDS_URL:
                total = player["statistics"][0]["cards"]["red"]
                red_cards = total if total is not None else 0
                reds.append((team, name, red_cards))
            else:
                total = player["statistics"][0]["cards"]["yellow"]
                yellow_cards = total if total is not None else 0
                yellows.append((team, name, yellow_cards))

    return scorers, assistants, reds, yellows
