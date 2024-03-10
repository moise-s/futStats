from fut_stats.config import (
    collection_matches,
    collection_players,
    collection_stats,
)
from fut_stats.models.models import Match, Player, StatsPlayer


def add_player(player_data: Player):
    if collection_players.find_one({"name": player_data.name}):
        return "Player already registered!"
    player = collection_players.insert_one(player_data.dict())
    return f"Successfully registered {player_data.name} with ID: {str(player.inserted_id)}"  # noqa


def player_exists(name: str) -> bool:
    """Check if a player exists in the players collection by name."""
    return collection_players.find_one({"name": name}) is not None


def all_players_exist(match_data: Match) -> bool:
    """Check if all players in the match exist in the players collection."""
    team_a_names = [player.name for player in match_data.team_a]
    team_b_names = [player.name for player in match_data.team_b]
    all_names = team_a_names + team_b_names
    return all(player_exists(name) for name in all_names)


def add_match(match_data: Match) -> str:
    """Add a match to the collection if all players exist."""

    # Check if all players exist
    if not all_players_exist(match_data):
        return "A player does not exist. Match not added."

    # Check if the match date already exists
    if collection_matches.find_one({"date": match_data.date}):
        return "A match with this date already exists. Match not added."

    match = collection_matches.insert_one(match_data.dict())

    # add a check if match was successfully added
    update_player_stats(match_data)

    return f"Successfully registered Match from {match_data.date} with ID: {str(match.inserted_id)}"  # noqa


def update_player_stats(match_data: Match) -> str:
    """Update the StatsPlayer for every player in the match."""
    team_a_win = match_data.goals_team_a > match_data.goals_team_b
    team_b_win = match_data.goals_team_b > match_data.goals_team_a
    draw = match_data.goals_team_a == match_data.goals_team_b
    current_players_names = [
        player.name for player in match_data.team_a + match_data.team_b
    ]

    # Update team A and B players
    for player in match_data.team_a + match_data.team_b:
        update_stats_for_player(
            player,
            team_win=player in match_data.team_a
            and team_a_win
            or player in match_data.team_b
            and team_b_win,
            draw=draw,
            team_loss=player in match_data.team_a
            and team_b_win
            or player in match_data.team_b
            and team_a_win,
            goal_difference=(
                (match_data.goals_team_a - match_data.goals_team_b)
                if player in match_data.team_a
                else (match_data.goals_team_b - match_data.goals_team_a)
            ),
        )

    update_stats_for_non_participating_players(current_players_names)

    return "Player stats updated successfully."

def update_stats_for_non_participating_players(current_players_names: list):
    all_player_names = [player["name"] for player in collection_players.find()]
    non_participating_players_names = [
        name for name in all_player_names if name not in current_players_names
    ]

    # Update overall_performance for players not in the current match
    for name in non_participating_players_names:
        player_stats = collection_stats.find_one({"player.name": name})
        if not player_stats:
            continue  # Skip if there's no stats for this player

        points_possible = points_possible_of_all_games()
        player_stats["overall_performance"] = (
            player_stats["points"] / points_possible if points_possible else 0
        )
        collection_stats.update_one(
            {"player.name": name},
            {"$set": {"overall_performance": player_stats["overall_performance"]}},
        )


def points_possible_of_all_games() -> int:
    """Count the number of matches in the collection_matches."""
    count = collection_matches.count_documents({})
    return count * 4


def update_stats_for_player(
    player: Player,
    team_win: bool,
    draw: bool,
    team_loss: bool,
    goal_difference: int,
):
    """Update or create StatsPlayer record for a single player."""
    stats = collection_stats.find_one({"player.name": player.name})
    if not stats:
        matches_played = 1
        points_won = 3 * int(team_win) + 1 * int(draw) + 1
        points_possible = 4
        stats = StatsPlayer(
            player=player,
            matches=matches_played,
            wins=int(team_win),
            draws=int(draw),
            losses=int(team_loss),
            points=points_won,
            goal_difference=goal_difference,
            overall_performance=points_won / points_possible_of_all_games(),
            relative_performance=points_won / points_possible,
        )
        collection_stats.insert_one(stats.dict())
    else:
        stats["matches"] += 1
        points_possible_of_played_games = stats["matches"] * 4
        stats["wins"] += int(team_win)
        stats["draws"] += int(draw)
        stats["losses"] += int(team_loss)
        points_for_this_match = 3 * int(team_win) + 1 * int(draw) + 1
        stats["points"] += points_for_this_match
        stats["goal_difference"] += goal_difference
        stats["overall_performance"] = stats["points"] / points_possible_of_all_games()
        stats["relative_performance"] = (
            stats["points"] / points_possible_of_played_games
        )
        collection_stats.update_one({"player.name": player.name}, {"$set": stats})
