from __future__ import annotations

from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from player_data import PlayerData

import flask

from database import initialize_database
from player_manager import PlayerDataManager

app = flask.Flask(__name__)
player_manager = PlayerDataManager()


# 註冊路由
@app.route("/")
def index():
    return flask.render_template("index.html")


@app.route("/api/player", methods=["GET"])
def get_player():
    # 搜尋
    player_id = flask.request.args.get("player_id")
    player_name = flask.request.args.get("player_name")
    mode = flask.request.args.get("mode")

    if mode == "search":
        # 搜尋玩家
        if not player_id and not player_name:
            return flask.jsonify({"error": "Missing player_id or player_name parameter"}), 400
        if player_id:
            if (player := player_manager.get_player(player_id)) is None:
                return flask.jsonify({"error": "Player not found"}), 404
            filtered_players = [player]
        elif player_name:
            filtered_players = player_manager.get_player_by_name(player_name)
            if not filtered_players:
                return flask.jsonify({"error": "Player not found"}), 404

    elif mode == "filter":
        # 篩選
        try:
            min_level = get_int_parameter("min_level")
        except ValueError:
            return flask.jsonify({"error": "Invalid min_level parameter"}), 400
        try:
            max_level = get_int_parameter("max_level")
        except ValueError:
            return flask.jsonify({"error": "Invalid max_level parameter"}), 400
        try:
            min_score = get_int_parameter("min_score")
        except ValueError:
            return flask.jsonify({"error": "Invalid min_score parameter"}), 400
        try:
            max_score = get_int_parameter("max_score")
        except ValueError:
            return flask.jsonify({"error": "Invalid max_score parameter"}), 400

        # 驗證篩選條件
        valid, error_message = validate_filter_parameters(min_level, max_level, min_score, max_score)
        if not valid:
            return flask.jsonify({"error": error_message}), 400

        # 確認玩家列表
        players: list[PlayerData] | None = None
        if not player_id and not player_name and all(value is None for value in (min_level, max_level, min_score, max_score)):
            return flask.jsonify({"error": "Missing any filter parameters"}), 400
        if player_id:
            if (player := player_manager.get_player(player_id)) is None:
                return flask.jsonify({"error": "Player not found"}), 404
            players = [player]
        elif player_name:
            players = player_manager.get_player_by_name(player_name)
            if not players:
                return flask.jsonify({"error": "Player not found"}), 404

        filtered_players = player_manager.filter_players(
            players=players,
            min_level=min_level,
            max_level=max_level,
            min_score=min_score,
            max_score=max_score,
        )

    else:
        return flask.jsonify({"error": "Invalid mode"}), 400

    return (
        flask.jsonify(
            {
                "count": len(filtered_players),
                "players": [player.to_dict() for player in filtered_players],
            }
        ),
        200,
    )


def get_int_parameter(name: str | None) -> int | None:
    name = flask.request.args.get(name)
    if name is not None:
        return int(name)
    else:
        return None


def validate_filter_parameters(min_level: int | None, max_level: int | None, min_score: int | None, max_score: int | None):
    if min_level is not None and max_level is not None and min_level > max_level:
        return False, "Invalid level range"

    if min_score is not None and max_score is not None and min_score > max_score:
        return False, "Invalid score range"

    return True, ""


initialize_database()
if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000)
