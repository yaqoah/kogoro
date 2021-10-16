from bot import PREDICTIONS_URL, LOGGER
from bot.utils.interpret import url_to_base64, base64_to_image, image_to_base64
import bot.proxy as api


async def predict(fid):
    query = {
        "fixture": fid
    }
    prediction = (await api.link(PREDICTIONS_URL, query))[0]

    winner = prediction["predictions"]["winner"]["name"]
    winnerID = prediction["predictions"]["winner"]["id"]
    for team in prediction["teams"]:
        if prediction["teams"][team]["id"] == winnerID:
            winside = team
        else:
            loseside = team

    if prediction["predictions"]["win_or_draw"]:
        advise = "A tie is conceivable with lower chances."
    else:
        advise = ""

    logoURL = url_to_base64(prediction["teams"][winside]["logo"])
    try:
        logoPIL = base64_to_image(logoURL)
        logoPIL.thumbnail((300, 300))
        logoURL = bytes(f"data:image/{logoPIL.format};base64,",
                        encoding="utf-8") + image_to_base64(logoPIL)
        interpretedURL = logoURL.decode("utf-8")
    except:
        LOGGER.info("resized image (api) unrecognized by pyrogram.")
    finally:
        interpretedURL = prediction["teams"][winside]["logo"]

    poi = prediction["comparison"]["poisson_distribution"][winside].split("%")[0]
    home_attacking = prediction["comparison"]["att"][winside].split("%")[0]
    away_attacking = prediction["comparison"]["att"][loseside].split("%")[0]
    home_defending = prediction["comparison"]["def"][winside].split("%")[0]
    away_defending = prediction["comparison"]["def"][loseside].split("%")[0]
    hatt = int(home_attacking) if home_attacking is not None else 0
    aatt = int(away_attacking) if away_attacking is not None else 0
    hdef = int(home_defending) if home_defending is not None else 0
    adef = int(away_defending) if away_defending is not None else 0
    odds = int(poi) or "N/A"

    if hatt > aatt:
        attacking = winner
    elif hatt == aatt:
        attacking = "No team"
    else:
        attacking = prediction["teams"][loseside]["name"]

    if hdef > adef:
        defending = winner
    elif hdef == adef:
        defending = "No team"
    else:
        defending = prediction["teams"][loseside]["name"]

    if prediction["predictions"]["under_over"]:
        total_goals = round(abs(float(prediction["predictions"]["under_over"])))
    else:
        total_goals = "N/A"

    return (
        winner, interpretedURL, odds,
        advise, attacking, defending,
        total_goals, interpretedURL
    )

