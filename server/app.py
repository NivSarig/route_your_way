from fastapi import BackgroundTasks, FastAPI, HTTPException
from dotenv import load_dotenv
from typing import List
from game import add_contestant, add_submit, create_game, get_game


load_dotenv()
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


@app.put("/game/{game_id}/submit")
async def submit(game_id: str, name: str, coordinates: List[List[float]], background_tasks: BackgroundTasks):
    curr_game = get_game(game_id)
    if not name:
        # create an exception
        raise HTTPException(status_code=400, detail="Name cannot be empty")
    if not coordinates:
        raise HTTPException(status_code=400, detail="coordinates cannot be empty")
    curr_contestant = curr_game["contestants"][name]
    if "status" in curr_contestant and curr_contestant["status"] == "processing":
        raise HTTPException(status_code=400, detail="Contestant already submitted")
    curr_contestant["status"] = "processing"
    background_tasks.add_task(add_submit, game_id, name, coordinates)
    return curr_game
