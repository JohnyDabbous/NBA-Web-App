# backend/app.py

from flask import Flask, request, jsonify
from flask_cors import CORS
from db_operations import db_operations

app = Flask(__name__)
CORS(app)  # allow requests from your Vite dev server

# Single shared DB object
db = db_operations()


# ---------- helpers ----------

def rows_to_dicts(columns, rows):
    """Zip column names with row tuples into list[dict]."""
    return [dict(zip(columns, row)) for row in rows]


# ---------- basic health check ----------

@app.route("/api/health")
def health():
    return jsonify({"status": "ok"})


# ---------- TOP 10 QUERIES ----------

@app.route("/api/players/top/points")
def top_players_points():
    query = """
        SELECT
            Player.PlayerID,
            Player.Name,
            AVG(PlayerGameStatistics.Points) AS avg_points
        FROM Player
        JOIN PlayerGameStatistics ON Player.PlayerID = PlayerGameStatistics.PlayerID
        GROUP BY Player.PlayerID, Player.Name
        ORDER BY avg_points DESC
        LIMIT 10;
    """
    rows = db.select_query(query)
    data = [
        {"player_id": r[0], "name": r[1], "avg_points": float(r[2])}
        for r in rows
    ]
    return jsonify(data)


@app.route("/api/players/top/assists")
def top_players_assists():
    query = """
        SELECT
            Player.PlayerID,
            Player.Name,
            AVG(PlayerGameStatistics.Assists) AS avg_assists
        FROM Player
        JOIN PlayerGameStatistics ON Player.PlayerID = PlayerGameStatistics.PlayerID
        GROUP BY Player.PlayerID, Player.Name
        ORDER BY avg_assists DESC
        LIMIT 10;
    """
    rows = db.select_query(query)
    data = [
        {"player_id": r[0], "name": r[1], "avg_assists": float(r[2])}
        for r in rows
    ]
    return jsonify(data)


@app.route("/api/players/top/rebounds")
def top_players_rebounds():
    query = """
        SELECT
            Player.PlayerID,
            Player.Name,
            AVG(PlayerGameStatistics.Rebounds) AS avg_rebounds
        FROM Player
        JOIN PlayerGameStatistics ON Player.PlayerID = PlayerGameStatistics.PlayerID
        GROUP BY Player.PlayerID, Player.Name
        ORDER BY avg_rebounds DESC
        LIMIT 10;
    """
    rows = db.select_query(query)
    data = [
        {"player_id": r[0], "name": r[1], "avg_rebounds": float(r[2])}
        for r in rows
    ]
    return jsonify(data)


# ---------- TEAM QUERIES ----------

@app.route("/api/team/roster")
def team_roster():
    team_name = request.args.get("team_name")
    if not team_name:
        return jsonify({"error": "team_name is required"}), 400

    query = """
        SELECT Player.PlayerID, Player.Name, Player.Position, Player.Age
        FROM Player
        INNER JOIN Team ON Player.TeamID = Team.TeamID
        WHERE Team.Name = %s;
    """
    rows = db.select_query_params(query, (team_name,))
    cols = ["player_id", "name", "position", "age"]
    return jsonify(rows_to_dicts(cols, rows))


# optional: search team players by position
@app.route("/api/team/players-by-position")
def team_players_by_position():
    team_name = request.args.get("team_name")
    position = request.args.get("position")
    if not team_name or not position:
        return jsonify({"error": "team_name and position are required"}), 400

    query = """
        SELECT Player.PlayerID, Player.Name, Player.Position, Player.Age
        FROM Player
        INNER JOIN Team ON Player.TeamID = Team.TeamID
        WHERE Team.Name = %s AND Player.Position = %s;
    """
    rows = db.select_query_params(query, (team_name, position))
    cols = ["player_id", "name", "position", "age"]
    return jsonify(rows_to_dicts(cols, rows))


# ---------- PLAYER QUERIES ----------

@app.route("/api/player/search")
def search_player_by_name():
    name = request.args.get("name")
    if not name:
        return jsonify({"error": "name is required"}), 400

    query = """
        SELECT PlayerID, Name, Height, Weight, Age, Position, TeamID
        FROM Player
        WHERE Name = %s;
    """
    rows = db.select_query_params(query, (name,))
    cols = ["player_id", "name", "height", "weight", "age", "position", "team_id"]
    return jsonify(rows_to_dicts(cols, rows))


# ---------- ADD / UPDATE ----------

@app.route("/api/team", methods=["POST"])
def add_team():
    data = request.json or {}
    required = ["name", "city", "division", "conference"]
    missing = [f for f in required if f not in data]
    if missing:
        return jsonify({"error": f"Missing fields: {', '.join(missing)}"}), 400

    query = """
        INSERT INTO Team (Name, City, Division, Conference)
        VALUES (%s, %s, %s, %s);
    """
    params = (data["name"], data["city"], data["division"], data["conference"])
    db.modify_query_params(query, params)
    return jsonify({"status": "ok"}), 201


@app.route("/api/player", methods=["POST"])
def add_player():
    data = request.json or {}
    required = ["name", "height", "weight", "age", "position", "team_id"]
    missing = [f for f in required if f not in data]
    if missing:
        return jsonify({"error": f"Missing fields: {', '.join(missing)}"}), 400

    query = """
        INSERT INTO Player (Name, Height, Weight, Age, Position, TeamID)
        VALUES (%s, %s, %s, %s, %s, %s);
    """
    params = (
        data["name"],
        int(data["height"]),
        int(data["weight"]),
        int(data["age"]),
        data["position"],
        int(data["team_id"]),
    )
    db.modify_query_params(query, params)
    return jsonify({"status": "ok"}), 201


@app.route("/api/player", methods=["PUT"])
def update_player():
    data = request.json or {}
    required = ["player_id", "column", "new_value"]
    missing = [f for f in required if f not in data]
    if missing:
        return jsonify({"error": f"Missing fields: {', '.join(missing)}"}), 400

    allowed_cols = {"Name", "Height", "Weight", "Age", "Position", "TeamID"}
    column = data["column"]
    if column not in allowed_cols:
        return jsonify({"error": f"Invalid column '{column}'"}), 400

    query = f"UPDATE Player SET {column} = %s WHERE PlayerID = %s;"
    params = (data["new_value"], int(data["player_id"]))
    db.modify_query_params(query, params)
    return jsonify({"status": "ok"})


@app.route("/api/team", methods=["PUT"])
def update_team():
    data = request.json or {}
    required = ["team_id", "column", "new_value"]
    missing = [f for f in required if f not in data]
    if missing:
        return jsonify({"error": f"Missing fields: {', '.join(missing)}"}), 400

    allowed_cols = {"Name", "City", "Division", "Conference"}
    column = data["column"]
    if column not in allowed_cols:
        return jsonify({"error": f"Invalid column '{column}'"}), 400

    query = f"UPDATE Team SET {column} = %s WHERE TeamID = %s;"
    params = (data["new_value"], int(data["team_id"]))
    db.modify_query_params(query, params)
    return jsonify({"status": "ok"})


# ---------- LOG PLAYER GAME (very simple version) ----------

@app.route("/api/player/log-game", methods=["POST"])
def log_player_game():
    data = request.json or {}
    required = ["game_id", "player_id", "points", "rebounds", "assists"]
    missing = [f for f in required if f not in data]
    if missing:
        return jsonify({"error": f"Missing fields: {', '.join(missing)}"}), 400

    query = """
        INSERT INTO PlayerGameStatistics
        (GameID, PlayerID, Points, Rebounds, Assists, Blocks, Steals, Turnovers, MinutesPlayed, Fouls)
        VALUES (%s, %s, %s, %s, %s, 0, 0, 0, 0, 0);
    """
    params = (
        int(data["game_id"]),
        int(data["player_id"]),
        int(data["points"]),
        int(data["rebounds"]),
        int(data["assists"]),
    )
    db.modify_query_params(query, params)
    return jsonify({"status": "ok"}), 201


if __name__ == "__main__":
    # run on http://localhost:5000
    app.run(debug=True)
