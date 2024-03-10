from typing import List
import json
from fut_stats.models.models import Match, Player
import pandas as pd

def create_matches_from_csv(file_path: str) -> List[Match]:
    df = pd.read_csv(file_path, sep=';')
    matches = []

    # Assuming each row is a player and each column is a match date (starting from column 2 for actual matches)
    for date_idx, date in enumerate(df.columns[1:], start=1):  # Skipping the player name column
        # Reset teams and scores for each match date
        team_a = []
        team_b = []
        goals_team_a = 0
        goals_team_b = 0
        goals_team_a = int(df.iloc[-2, date_idx])
        goals_team_b = int(df.iloc[-1, date_idx])  

        for row in df.itertuples(index=False):
            # print(row)
            # input('.')
            player_name = row[0]  # First column is player names
            player_result = getattr(row, f'_{date_idx}')  # Access the result by dynamic attribute

            if player_result == 'v':
                team_a.append(Player(name=player_name))
            elif player_result == 'd':
                team_b.append(Player(name=player_name))
            elif player_result == 'e':
                team_a.append(Player(name=player_name))

        match = Match(date=date, team_a=team_a, team_b=team_b, goals_team_a=goals_team_a, goals_team_b=goals_team_b)
        matches.append(match)

    return matches

def match_to_dict(match):
    return {
        "date": match.date.strftime('%Y-%m-%dT%H:%M:%S'),  # Convert datetime to string
        "team_a": [player.name for player in match.team_a],
        "team_b": [player.name for player in match.team_b],
        "goals_team_a": match.goals_team_a,
        "goals_team_b": match.goals_team_b
    }

#  USAGE:
file_path = 'fut_2023.csv'
matches = create_matches_from_csv(file_path)
matches_dict = [match_to_dict(match) for match in matches]
json_file_path = 'fut_2023.json'
with open(json_file_path, 'w', encoding='utf-8') as f:
    json.dump(matches_dict, f, ensure_ascii=False, indent=4)

