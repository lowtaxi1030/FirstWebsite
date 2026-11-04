import sqlite3


def get_connection() -> sqlite3.Connection:
    return sqlite3.connect("players.db")


def initialize_database():
    connection = get_connection()
    connection.execute("""
        CREATE TABLE IF NOT EXISTS players (
            player_id TEXT PRIMARY KEY,
            name TEXT NOT NULL,
            level INTEGER DEFAULT 1,
            score INTEGER DEFAULT 0
        );  """)
    connection.commit()
    connection.close()
