from bot import bot, LOGGER
from bot.message import *
from bot.callback import *

try:
    bot.run()
    LOGGER.info("bot start!")
except ConnectionError:
    LOGGER.error("bot already running.")
