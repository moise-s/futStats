from datetime import datetime
from typing import List, Optional

from pydantic import BaseModel


class Player(BaseModel):
    name: str


class Match(BaseModel):
    date: datetime
    team_a: Optional[List[Player]]
    team_b: Optional[List[Player]]
    goals_team_a: int
    goals_team_b: int

    class Config:
        schema_extra = {
            "example": {
                "date": "2024-03-07T14:30:00",
                "team_a": [{"name": "Player 1"}],
                "team_b": [{"name": "Player 2"}],
                "goals_team_a": 3,
                "goals_team_b": 2,
            }
        }


class StatsPlayer(BaseModel):
    player: Player
    matches: int = 0
    wins: int = 0
    draws: int = 0
    losses: int = 0
    points: int = 0
    goal_difference: int = 0
    overall_performance: Optional[float] = None
    relative_performance: Optional[float] = None
