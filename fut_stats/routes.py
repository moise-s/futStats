from database import add_player
from fastapi import FastAPI
from models import Player

app = FastAPI()


@app.post("/players/", response_description="Add new player", response_model=Player)
async def create_player(player: Player):
    player_id = add_player(player.dict())
    if not player_id:
        pass
