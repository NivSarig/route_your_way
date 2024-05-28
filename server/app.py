from fastapi import BackgroundTasks, FastAPI, HTTPException

import sys, os
from game import add_contestant, add_submit, create_game, get_game

sys.path.append(os.getcwd() + "/..")

from external_integrations.gmaps_integration_utils import generate_random_coordinates

app = FastAPI()


@app.get("/")
async def root():
    return {"message": "Hello World"}


@app.put("/game")
async def put_game(location: str = None):
    return create_game(location)


@app.put("/game/{game_id}/contestant")
async def put_contestant(game_id: str = None, name: str = None):
    get_game(game_id)
    if not name:
        # create an exception
        raise HTTPException(status_code=400, detail="Name cannot be empty")
    add_contestant(game_id, name)
    return get_game(game_id)


@app.put("/game/{game_id}/done")
async def put_done(game_id: str = None):
    game = get_game(game_id)
    game["status"] = "done"
    return game


# endpoint that returns a game
@app.get("/game/{game_id}")
async def get_game_endpoint(game_id: str = None):
    return get_game(game_id)


@app.put("/game/{game_id}/submit/{url}")
async def submit(game_id: str, name: str, url: str, background_tasks: BackgroundTasks):
    curr_game = get_game(game_id)
    if not name:
        # create an exception
        raise HTTPException(status_code=400, detail="Name cannot be empty")
    if not url:
        raise HTTPException(status_code=400, detail="URL cannot be empty")
    curr_contestant = curr_game["contestants"][name]
    if "status" in curr_contestant and curr_contestant["status"] == "processing":
        raise HTTPException(status_code=400, detail="Contestant already submitted")
    curr_contestant["status"] = "processing"
    background_tasks.add_task(add_submit, game_id, name, url)
    return curr_game
