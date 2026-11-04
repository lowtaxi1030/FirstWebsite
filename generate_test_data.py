import random


def generate_random_player(player_id) -> dict:
    names = ["Alice", "Bob", "Charlie", "David", "Eve"]
    name = random.choice(names)
    level = random.randint(1, 100)
    score = random.randint(0, 10000)
    return {
        "player_id": player_id,
        "name": name,
        "level": level,
        "score": score,
    }


def generate_random_players(count):
    for i in range(count):
        player_id = f"Player{i+1:03d}"
        player_data = generate_random_player(player_id)
        yield player_data
