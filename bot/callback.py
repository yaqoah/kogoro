# -*- coding: utf-8 -*-
from bot import (bot, PREDICTION_MESSAGE, LEAGUE_STATS_MESSAGE,
                 TEAM_STATS_MESSAGE, PLAYER_STATS_MESSAGE, LOGGER)
import bot.proxy as proxy
from bot.proxy.team import team_statistics
from bot.proxy.match import predict
from bot.proxy.league import league_statistics
from bot.proxy.player import player_statistics
from bot.utils.filters import custom_filters
import bot.message as msg
from pyrogram import Client
from pyrogram.errors import BadRequest
from pyrogram.types import (CallbackQuery, InlineKeyboardMarkup,
                            InlineKeyboardButton)


@bot.on_callback_query(custom_filters.start_commands_filter)
async def panel(_, cbq: CallbackQuery):
    msg.task = cbq.data
    await cbq.message.reply_text(
        "Enter the season year (e.g.: 2021)",
        parse_mode="markdown",
        disable_notification=False
    )


@bot.on_callback_query(custom_filters.fixture_id_filter)
async def opponent(app: Client, cbq: CallbackQuery):
    fixture_id = cbq.data.split("_")[1]
    prediction = await predict(fixture_id)

    winner = prediction[0]
    if winner:
        outcome_message = f"{winner} will win 🥇"
    else:
        outcome_message = "It will end in a draw ❗️😖"

    logo = prediction[1]
    probability = prediction[2]

    advise = prediction[3]
    if advise:
        advise_message = f"💊 {advise}"
    else:
        advise_message = "🌨🌨🌨🌨🌨🌨🌨🌨🌨"

    attacking_team = prediction[4]
    defending_team = prediction[5]
    goals = prediction[6]
    logo = prediction[7]

    await cbq.message.reply_photo(logo)
    LOGGER.info("photo posted")

    await cbq.message.reply_text(
        PREDICTION_MESSAGE.format(outcome_message,
                                  probability,
                                  advise_message,
                                  attacking_team,
                                  defending_team,
                                  goals),
        parse_mode="markdown",
        disable_notification=False)


@bot.on_callback_query(custom_filters.league_id_filter)
async def league(app: Client, cbq: CallbackQuery):
    league_id = cbq.data.split("_")[1]
    league_name = cbq.data.split("_")[2]
    goal, assists, red, yellow = await league_statistics(league_id)
    try:
        fmost_g,  smost_g, tmost_g = goal
        fmost_a, smost_a, tmost_a = assists
        fmost_r, smost_r, tmost_r = red
        fmost_y, smost_y, tmost_y = yellow

        await cbq.message.reply_text(
            LEAGUE_STATS_MESSAGE.format(league_name, proxy.season,
                                        *fmost_g, *smost_g, *tmost_g,
                                        *fmost_a, *smost_a, *tmost_a,
                                        *fmost_r, *smost_r, *tmost_r,
                                        *fmost_y, *smost_y, *tmost_y),
            parse_mode="markdown",
            disable_notification=False
        )
    except ValueError as ve:
        await cbq.message.reply_text(
            "No stats recorded. choose another!"
        )


@bot.on_callback_query(custom_filters.team_id_filter)
async def team(app: Client, cbq: CallbackQuery):
    league_id = int(cbq.data.split("_")[1])
    team_statistic = await team_statistics(league_id)
    logo = team_statistic[0]
    name = team_statistic[1]
    form = team_statistic[2]
    win_draw_lose = team_statistic[3]
    goals_for = team_statistic[4]
    for_period = team_statistic[5]
    goals_against = team_statistic[6]
    against_period = team_statistic[7]
    streak_ls = team_statistic[8]
    failed_to_score = team_statistic[9]
    streak_ws = team_statistic[10]
    clean_sheets = team_statistic[11]

    await cbq.message.reply_photo(logo)
    LOGGER.info("photo posted")

    try:
        await cbq.message.reply_text(
            TEAM_STATS_MESSAGE.format(
                name, proxy.season, form,
                win_draw_lose[0], win_draw_lose[1], win_draw_lose[2],
                goals_for, for_period, goals_against, against_period,
                streak_ls, failed_to_score, name, streak_ws, clean_sheets
            ),
            parse_mode="markdown",
            disable_notification=False
        )
    except BadRequest:
        LOGGER.info("team stats in this league are not fetched from API")
        await cbq.message.reply_text("error. try another call.")


@bot.on_callback_query(custom_filters.player_id_filter)
async def player(app: Client, cbq: CallbackQuery):
    player_id = int(cbq.data.split("_")[1])
    league_to_select_from = await player_statistics(player_id)
    gahz = [
        [
            InlineKeyboardButton(f"{league_name}",
                                 callback_data=f"plid_{player_id}_{league_id}")
        ] for league_id, league_name in league_to_select_from.items()
    ]
    gahz.append(
        [
            InlineKeyboardButton("ALL",
                                 callback_data=f"plid_{player_id}_1999")
        ]
    )
    await cbq.message.reply_text("Alright, choose league, "
                                 "or 'all' if player's season stats ⬇️",
                                 parse_mode="markdown",
                                 reply_markup=InlineKeyboardMarkup(gahz)
                                 )


@bot.on_callback_query(custom_filters.player_league_id_filter)
async def nominate(app: Client, cbq: CallbackQuery):
    player_id = cbq.data.split("_")[1]
    league_id = cbq.data.split("_")[2]

    try:
        league_id = float(league_id)
    except ValueError:
        league_id = int(str(league_id))
    else:
        league_id = int(league_id)

    stats = (await player_statistics(player_id, league_id))
    about = stats[0]
    shots = stats[1]
    passes = stats[2]
    defending = stats[3]
    dribbling = stats[4]
    foul_play = stats[5]
    logo = stats[6]

    await cbq.message.reply_photo(logo)
    LOGGER.info("photo posted")

    try:
        await cbq.message.reply_text(
            PLAYER_STATS_MESSAGE.format(*about, *shots, *passes, *defending,
                                        *dribbling, *foul_play),
            parse_mode="markdown",
            disable_notification=False
        )
    except BadRequest as bd:
        LOGGER.debug("one parameter of player in league returns None."
                     "prior exception failed.")
        await cbq.message.reply_text("error. try another call.")

