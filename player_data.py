class PlayerData:
    def __init__(self, player_id: str, player_name: str, level: int = 1, score: int = 0):
        self.player_id = player_id
        self.name = player_name
        self.level = level
        self.score = score

    def __repr__(self):
        return f"PlayerData(player_id: {self.player_id}, name: {self.name}, level: {self.level}, score: {self.score})"

    def to_dict(self) -> dict:
        return {
            "player_id": self.player_id,
            "name": self.name,
            "level": self.level,
            "score": self.score,
        }
