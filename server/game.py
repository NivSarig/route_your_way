game_dict = {}
from utils import generate_random_string
from fastapi import HTTPException


def get_game(game_id):
    # throw exception if game_id doesn't exist
    if game_id not in game_dict:
        raise HTTPException(status_code=404, detail="Game not found")
    return game_dict[game_id]


def create_game(location, code=None):

    new_game_id = code or generate_random_string()
    print("creating game", new_game_id)

    game_dict[new_game_id] = {
        "location": location,
        "game_id": new_game_id,
        "contestants": {},
        "status": "running",
    }

    return get_game(new_game_id)


def verify_existing_name(game_id, name):
    if name not in get_game(game_id)["contestants"]:
        raise HTTPException(status_code=400, detail="Contestant doesn't exists")

def verify_unique_name(game_id, name):
    if name in get_game(game_id)["contestants"]:
        raise HTTPException(status_code=400, detail="Contestant already exists (name is taken)")

def add_contestant(game_id, name):
    verify_unique_name(game_id, name)

    game_dict[game_id]["contestants"][name] = {"name": name}
    return get_game(game_id)

def add_submit(game_id, name, url):
    curr_game = get_game(game_id)
    verify_existing_name(game_id, name)
    duration = 444 #get_duration(url)
    curr_game["contestants"][name]["duration"] = duration
    curr_game["contestants"][name]["url"] = url
    return get_game(game_id)

create_game("TEST", "TEST")
