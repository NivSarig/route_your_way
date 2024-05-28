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
