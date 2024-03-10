# Football Match & Player Stats API

## Overview

This API provides functionality to manage football matches and player statistics. It allows users to create match records, retrieve match data, and manage player statistics including wins, losses, draws, points, goal difference, and performance metrics.

## Models

### **Match**

Represents a football match, including the participating teams, match date, and goals scored by each team.

- **Fields:**
  - `date`: The date and time of the match.
  - `team_a`: List of `Player` objects representing the first team.
  - `team_b`: List of `Player` objects representing the second team.
  - `goals_team_a`: Goals scored by Team A.
  - `goals_team_b`: Goals scored by Team B.

### **Player**

Describes a player, including their name and potentially other attributes like age and position (not implemented yet).

### **StatsPlayer**

Tracks a player's statistics across matches.

- **Fields:**
  - `player`: A `Player` object representing the individual player.
  - `matches`: Total number of matches played.
  - `wins`: Total number of wins.
  - `draws`: Total number of draws.
  - `losses`: Total number of losses.
  - `points`: Total points accumulated.
  - `goal_difference`: Goal difference (goals scored minus goals conceded).
  - `overall_performance`: Calculated metric of overall performance.
  - `relative_performance`: Calculated metric of performance relative to others.

## API Endpoints

### Match Endpoints

- **POST /match**: Create a new match record.

### Player Stats Endpoints

Not implemented yet.

## Usage

### Creating a Match

To create a match, send a POST request to `/match` with a JSON body containing the match details, such as date, teams, and goals scored by each team.

#### Example Request

```json
{
  "date": "2024-03-07T14:30:00",
  "team_a": [{"name": "Player 1"}],
  "team_b": [{"name": "Player 2"}],
  "goals_team_a": 3,
  "goals_team_b": 2
}
