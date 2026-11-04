from __future__ import annotations

import sqlite3

from database import get_connection
from player_data import PlayerData


class PlayerDataManager:

    def add_player(self, player_data: PlayerData) -> bool:
        connection = get_connection()
        try:
            connection.execute(
                """
                INSERT INTO players (player_id, name, level, score)
                VALUES (?, ?, ?, ?);
                """,
                (
                    player_data.player_id,
                    player_data.name,
                    player_data.level,
                    player_data.score,
                ),
            )
            connection.commit()
        except sqlite3.IntegrityError:
            return False
        finally:
            connection.close()
        return True

    def filter_players(
        self,
        players: list[PlayerData] | None = None,
        min_level: int | None = None,
        max_level: int | None = None,
        min_score: int | None = None,
        max_score: int | None = None,
    ) -> list[PlayerData]:

        # 給SQLite篩選
        if players is None:
            connection = get_connection()
            try:

                conditions = []
                values = []

                if min_level is not None:
                    conditions.append("level >= ?")
                    values.append(min_level)

                if max_level is not None:
                    conditions.append("level <= ?")
                    values.append(max_level)

                if min_score is not None:
                    conditions.append("score >= ?")
                    values.append(min_score)

                if max_score is not None:
                    conditions.append("score <= ?")
                    values.append(max_score)

                cursor = connection.execute(
                    f"""
                    SELECT * FROM players
                    {("WHERE " + " AND ".join(conditions)) if conditions else ""};
                    """,
                    values,
                )
                results = cursor.fetchall()
                return [PlayerData(*r) for r in results]

            finally:
                connection.close()

        # python自己篩選
        else:
            return [
                player
                for player in players
                if (
                    (min_level is None or player.level >= min_level)
                    and (max_level is None or player.level <= max_level)
                    and (min_score is None or player.score >= min_score)
                    and (max_score is None or player.score <= max_score)
                )
            ]

    def get_player(self, player_id: str, connection: sqlite3.Connection | None = None) -> PlayerData | None:
        is_connection_owner = False
        try:
            if connection is None:
                connection = get_connection()
                is_connection_owner = True
            cursor = connection.execute(
                """
                SELECT * FROM players
                WHERE player_id = ?;
                """,
                (player_id,),
            )
            if (result := cursor.fetchone()) is None:
                return None
            return PlayerData(*result)
        finally:
            if is_connection_owner:
                connection.close()

    def get_player_by_name(self, player_name: str) -> list[PlayerData]:
        connection = get_connection()
        try:
            cursor = connection.execute(
                """
                SELECT * FROM players
                WHERE name = ?;
                """,
                (player_name,),
            )
            results = cursor.fetchall()
            return [PlayerData(*r) for r in results]
        finally:
            connection.close()

    def get_all_players() -> list[PlayerData]:
        connection = get_connection()
        try:
            cursor = connection.execute(
                """
                SELECT * FROM players
                """,
            )
            results = cursor.fetchall()
            return [PlayerData(*r) for r in results]
        finally:
            connection.close()

    def update_player(
        self,
        player_id: str,
        new_name: str | None = None,
        new_level: int | None = None,
        new_score: int | None = None,
    ) -> PlayerData | None:

        connection = get_connection()
        try:

            if (new_player := self.get_player(player_id, connection)) is None:
                return None

            update_fields = []
            values = []

            if new_name is not None:
                update_fields.append("name = ?")
                values.append(new_name)
            if new_level is not None:
                update_fields.append("level = ?")
                values.append(new_level)
            if new_score is not None:
                update_fields.append("score = ?")
                values.append(new_score)

            if not update_fields:
                return new_player

            connection.execute(
                f"""
                UPDATE players
                SET {", ".join(update_fields)}
                WHERE player_id = ?;
                """,
                (*values, player_id),
            )
            connection.commit()

        finally:
            connection.close()

        if new_name is not None:
            new_player.name = new_name
        if new_level is not None:
            new_player.level = new_level
        if new_score is not None:
            new_player.score = new_score

        return new_player

    def remove_player(self, player_id: str) -> bool:

        connection = get_connection()
        try:
            if (del_player := self.get_player(player_id, connection)) is not None:
                connection.execute(
                    """
                    DELETE FROM players
                    WHERE player_id = ?;
                    """,
                    (del_player.player_id,),
                )
                connection.commit()
                return True
        finally:
            connection.close()

        return False
