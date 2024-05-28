from fastapi import FastAPI, HTTPException

from game import add_contestant, create_game, get_game


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
