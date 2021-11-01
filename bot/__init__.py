import os
import sys
from logging import getLogger, basicConfig, DEBUG, INFO
from distutils.util import strtobool
from dotenv import load_dotenv
from pyrogram import Client
from pyrogram.errors import BadRequest

load_dotenv("../config.env")

LOGGER_VERBOSE = strtobool(os.environ.get("LOGGER_VERBOSE", "False"))

if LOGGER_VERBOSE:
    basicConfig(
        format="%(asctime)s - %(name)s - %(levelname)s - %(message)s",
        level=DEBUG
    )
else:
    basicConfig(
        format="%(asctime)s - %(name)s - %(levelname)s - %(message)s",
        level=INFO
    )

LOGGER = getLogger(__name__)


def get_config(name: str):
    return os.environ[name]


try:
    #  Connects to Telegram
    SESSION_NAME = get_config("SESSION_NAME")
    BOT_TOKEN = get_config("BOT_TOKEN")
    TELEGRAM_API = get_config("TELEGRAM_API")
    TELEGRAM_HASH = get_config("TELEGRAM_HASH")
    TELEGRAM_USERNAME = get_config("TELEGRAM_USERNAME")

    #  Connects to RapidAPI
    RAPID_API_HOST_REQ = get_config("RAPID_API_HOST_REQ")
    RAPID_API_KEY_REQ = get_config("RAPID_API_KEY_REQ")
    RAPID_API_HOST_VALUE = get_config("RAPID_API_HOST_VALUE")
    RAPID_API_KEY_VALUE = get_config("RAPID_API_KEY_VALUE")

    #  Connects to API-FOOTBALL
    TEAMSm_URL = get_config("TEAMS_URL")
    FIXTURES_URL = get_config("FIXTURES_URL")
    PREDICTIONS_URL = get_config("PREDICTIONS_URL")
    LEAGUES_URL = get_config("LEAGUES_URL")
    TOP_SCORERS_URL = get_config("TOP_SCORERS_URL")
    TOP_ASSISTS_URL = get_config("TOP_ASSISTS_URL")
    TOP_RED_CARDS_URL = get_config("TOP_RED_CARDS_URL")
    TOP_YELLOW_CARDS_URL = get_config("TOP_YELLOW_CARDS_URL")
    TEAM_STATS_URL = get_config("TEAM_STATS_URL")
    PLAYERS_URL = get_config("PLAYERS_URL")

    #  Preempted bot replies (f-string)
    WELCOME_MESSAGE = get_config("WELCOME_MESSAGE")
    TEAM_NAME_MESSAGE = get_config("TEAM_NAME_MESSAGE")
    DECADE_CLARIFY_MESSAGE = get_config("DECADE_CLARIFY_MESSAGE")
    INVALID_YEAR_MESSAGE = get_config("INVALID_YEAR_MESSAGE")
    SELECT_TEAM_MESSAGE = get_config("SELECT_TEAM_MESSAGE")
    PREDICTION_MESSAGE = get_config("PREDICTION_MESSAGE")
    LEAGUE_STATS_MESSAGE = get_config("LEAGUE_STATS_MESSAGE")
    TEAM_STATS_MESSAGE = get_config("TEAM_STATS_MESSAGE")
    PLAYER_STATS_MESSAGE = get_config("PLAYER_STATS_MESSAGE")

except KeyError as ke:
    LOGGER.error("check your .env or variables. exiting.")
    sys.exit(1)

try:
    bot = Client(SESSION_NAME, api_id=TELEGRAM_API, api_hash=TELEGRAM_HASH, bot_token=BOT_TOKEN)
except BadRequest as bd:
    LOGGER.info("(exiting) bot api_id & api_hash combination invalid or expired token.")
    sys.exit(1)
