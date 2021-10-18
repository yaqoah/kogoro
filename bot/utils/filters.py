from pyrogram import Client, filters
from pyrogram.types import CallbackQuery, Message


class custom_filters:
    class start_actions_filter:
        @staticmethod
        async def start_filter(self, client: Client, start: CallbackQuery) -> bool:
            return start.data.split("_")[0] == "start"

    start_commands_filter = filters.create(start_actions_filter.start_filter)

    class team_name_filter:
        @staticmethod
        async def club_filter(self, client: Client, message: Message) -> bool:
            return message["text"].split()[-1].lower() == "club"

        @staticmethod
        async def country_filter(self, client: Client, message: Message) -> bool:
            return (
                    message["text"].split(" ")[-2].lower() == "national"
                    or
                    message["text"].split(" ")[-2].lower() == "team"
                    )

    club_name_filter = filters.create(team_name_filter.club_filter)
    country_name_filter = filters.create(team_name_filter.country_filter)

    class season_filter:
        @staticmethod
        async def season_year_filter(_, __, message: Message) -> bool:
            try:
                int(message["text"])
            except ValueError:
                return False

            return True

    season_format_filter = filters.create(season_filter.season_year_filter)

    class unique_id_filter:
        @staticmethod
        async def fid_filter(_, __, callback: CallbackQuery) -> bool:
            return callback.data.split("_")[0] == "fid"

        @staticmethod
        async def lid_filter(_, __, callback: CallbackQuery) -> bool:
            return callback.data.split("_")[0] == "lid"

        @staticmethod
        async def tid_filter(_, __, callback: CallbackQuery) -> bool:
            return callback.data.split("_")[0] == "tid"

        @staticmethod
        async def pid_filter(_, __, callback: CallbackQuery) -> bool:
            return callback.data.split("_")[0] == "pid"

        @staticmethod
        async def plid_filter(_, __, callback: CallbackQuery) -> bool:
            return callback.data.split("_")[0] == "plid"

    fixture_id_filter = filters.create(unique_id_filter.fid_filter)
    league_id_filter = filters.create(unique_id_filter.lid_filter)
    team_id_filter = filters.create(unique_id_filter.tid_filter)
    player_id_filter = filters.create(unique_id_filter.pid_filter)
    player_league_id_filter = filters.create(unique_id_filter.plid_filter)
