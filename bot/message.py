# -*- coding: utf-8 -*-
import bot.proxy as proxy
from bot.proxy.team import name, all_players, all_leagues, compete, next_ten
from bot.utils.filters import custom_filters
from bot.utils.commands import mybots
from pyrogram import Client, filters
from pyrogram.types import Message, InlineKeyboardMarkup, InlineKeyboardButton
from bot import (bot, TELEGRAM_USERNAME, WELCOME_MESSAGE, DECADE_CLARIFY_MESSAGE,
                 TEAM_NAME_MESSAGE, INVALID_YEAR_MESSAGE, SELECT_TEAM_MESSAGE)
import datetime

task = str()


@bot.on_message(filters.command(mybots.CONTACT_COMMAND))
async def contact(app: Client, message: Message):
    await message.reply_text(f"@{TELEGRAM_USERNAME}")


@bot.on_message(filters.command(mybots.START_COMMAND))
async def start(app: Client, message: Message):
    await message.reply_text(
        WELCOME_MESSAGE.format(message.from_user.first_name),
        parse_mode="markdown",
        disable_notification=False,
        reply_markup=InlineKeyboardMarkup(
            [
                [
                    InlineKeyboardButton("🎯 Predict Outcome",
                                         callback_data="start_predict"),
                    InlineKeyboardButton("⚔️ League statistics",
                                         callback_data="start_league_stats")
                ],
                [
                    InlineKeyboardButton("🚩 Team statistics",
                                         callback_data="start_team_stats"),
                    InlineKeyboardButton("🏃🏾 Player statistics",
                                         callback_data="start_player_stats")
                ]
            ]
        )
    )


@bot.on_message(filters.command(mybots.PREDICT_COMMAND)
                | filters.command(mybots.LEAGUE_STATISTICS_COMMAND)
                | filters.command(mybots.TEAM_STATISTICS_COMMAND)
                | filters.command(mybots.PLAYER_STATISTICS_COMMAND))
async def command(_, message: Message):
    global task
    await message.reply_text(
        "Enter the season year (e.g.: 2021)",
        parse_mode="markdown",
        disable_notification=False
    )
    task = message["text"]


@bot.on_message(~ filters.command(mybots.CONTACT_COMMAND)
                & ~ filters.command(mybots.START_COMMAND)
                & ~ filters.command(mybots.PREDICT_COMMAND)
                & ~ filters.command(mybots.LEAGUE_STATISTICS_COMMAND)
                & ~ filters.command(mybots.TEAM_STATISTICS_COMMAND)
                & ~ filters.command(mybots.PLAYER_STATISTICS_COMMAND)
                & ~ custom_filters.season_format_filter
                & ~ custom_filters.club_name_filter
                & ~ custom_filters.country_name_filter)
async def no_context(_, message: Message):
    await message.reply_text(
        f"Sorry {message.from_user.first_name}. Unrecognized command.",
        parse_mode="markdown",
        disable_notification=False
    )


@bot.on_message(custom_filters.season_format_filter)
async def select(app: Client, year: Message):
    season_year = int(year["text"])
    current_year = int(datetime.datetime.now().year)
    if season_year < 2010:
        await year.reply_text(
            DECADE_CLARIFY_MESSAGE,
            parse_mode="markdown",
            disable_notification=False
        )
    elif season_year <= current_year:
        proxy.season = season_year
        await year.reply_text(
            TEAM_NAME_MESSAGE,
            parse_mode="markdown",
            disable_notification=False
        )
    else:
        await year.reply_text(
            INVALID_YEAR_MESSAGE.format(current_year),
            parse_mode="markdown",
            disable_notification=False
        )


@bot.on_message(custom_filters.club_name_filter
                | custom_filters.country_name_filter)
async def execute(app: Client, team: Message):
    squad = team["text"].lower().split(" ")
    if "club" in squad:
        squad.remove("club")
    else:
        squad.remove("national")
        squad.remove("team")

    is_team = await compete(" ".join(squad))
    if is_team:
        if "predict" in task:
            matches = await next_ten()
            total_games = range(len(dict(matches)))
            await team.reply_text(
                SELECT_TEAM_MESSAGE.format(squad),
                parse_mode="markdown",
                disable_notification=False,
                reply_markup=InlineKeyboardMarkup(
                    [
                        [
                            InlineKeyboardButton(
                                f"🆚 {list(matches.values())[left_index]}",
                                callback_data=f"fid_{list(matches.keys())[left_index]}"),
                            InlineKeyboardButton(
                                f"🆚 {list(matches.values())[right_index]}",
                                callback_data=f"fid_{list(matches.keys())[right_index]}")
                        ] for left_index, right_index in zip(total_games[0::2], total_games[1::2])
                    ]
                )
            )

        if "league" in task or "team" in task:
            competitions = await all_leagues()
            total_competitions = range(len(dict(competitions)))
            ltid = "lid" if "league" in task else "tid"

            await team.reply_text(
                "Alright, choose league for statistics👇",
                parse_mode="markdown",
                disable_notification=False,
                reply_markup=InlineKeyboardMarkup(
                    [
                        [
                           InlineKeyboardButton(
                               f"🏆 {competitions[league_id]} 🏆 ",
                               callback_data=f"{ltid}_{league_id}_{competitions[league_id]}")
                        ] for league_id in competitions
                    ]
                )
            )

        if "player" in task:
            players = await all_players()
            total_players = range(len(players))
            await team.reply_text(
                "Nice, who do you pick 💬",
                parse_mode="markdown",
                disable_notification=False,
                reply_markup=InlineKeyboardMarkup(
                    [
                        [
                            InlineKeyboardButton(
                                f"{list(players.values())[left_index]}",
                                callback_data=f"pid_{list(players.keys())[left_index]}"),
                            InlineKeyboardButton(
                                f"{list(players.values())[right_index]}",
                                callback_data=f"pid_{list(players.keys())[right_index]}")

                        ] for left_index, right_index in zip(total_players[0::2], total_players[1::2])
                    ]
                )
            )

    else:
        await team.reply_text(
            "Couldn't recognize team.. Try again 🔁",
            parse_mode="markdown",
            disable_notification=False
        )
