from dotenv import load_dotenv
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from mangum import Mangum

from fut_stats.models.models import Match, Player
from fut_stats.services import add_match, add_player

load_dotenv()

app = FastAPI(title="futStats!")

origins = [
    "*",
]
app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


@app.get("/")
def read_root():
    return {"Hello": "World"}


@app.post("/player/", response_description="Add new player")
async def create_player(player: Player) -> str:
    return add_player(player)


@app.post("/match/", response_description="Add new match")
async def create_match(player: Match) -> str:
    return add_match(player)


handler = Mangum(app=app)
