import mysql.connector

db = mysql.connector.connect(
    host="localhost",
    user="root",
    password="CPSC408!",
    database="NBA"
)
cursor = db.cursor()

def add_player(name, height, weight, age, position, team_id):
    query = '''
    INSERT INTO player (Name, Height, Weight, Age, Position, TeamID)
    VALUES (%s, %s, %s, %s, %s, %s'''
    cursor.execute(query, (name, height, weight, age, position, team_id))
    db.commit()

def delete_player(player_name): 
    query = '''
    DELETE FROM player
    WHERE Name = %s'''
    cursor.execute(query, (player_name,))
    db.commit()

def update_player(player_id, column, new_value):
    query = f'''
    UPDATE player
    SET {column} = %s
    WHERE PlayerID = %s'''
    cursor.execute(query, (new_value, player_id))
    db.commit()
    

def get_player(player_name):
    query = '''
    SELECT * FROM player
    WHERE Name = %s'''
    cursor.execute(query, (player_name,))
    return cursor.fetchall()

def get_players_by_team(team_name):
    query = '''
    SELECT * FROM player
    INNER JOIN Team ON players.TeamID = Team.TeamID
    WHERE Team.Name = %s'''
    cursor.execute(query, (team_name,))
    return cursor.fetchall()

def get_players_by_position(position):
    query = '''
    SELECT * FROM player
    WHERE Position = %s'''
    cursor.execute(query, (position,))
    return cursor.fetchall()


# -----------------------------
# TEAM CRUD
# -----------------------------
def add_team(name, city, division, conference):
    query = '''
    INSERT INTO Team (Name, City, Division, Conference)
    VALUES (%s, %s, %s, %s)'''
    cursor.execute(query, (name, city, division, conference))
    db.commit()

def delete_team(team_name):
    query = '''
    DELETE FROM Team
    WHERE Name = %s'''
    cursor.execute(query, (team_name,))
    db.commit()

def update_team(team_id, column, new_value):
    query = f'''
    UPDATE Team
    SET {column} = %s
    WHERE TeamID = %s'''
    cursor.execute(query, (new_value, team_id))
    db.commit()

def get_team(team_name):
    query = '''
    SELECT * FROM Team
    WHERE Name = %s'''
    cursor.execute(query, (team_name,))
    return cursor.fetchall()

def get_all_teams():
    query = '''
    SELECT * FROM Team'''
    cursor.execute(query)
    return cursor.fetchall()


# -----------------------------
# COACH CRUD
# -----------------------------
def add_coach(name, salary, team_id):
    query = '''
    INSERT INTO Coach (Name, Salary, TeamID)
    VALUES (%s, %s, %s)'''
    cursor.execute(query, (name, salary, team_id))
    db.commit()

def delete_coach(coach_name):
    query = '''
    DELETE FROM Coach
    WHERE Name = %s'''
    cursor.execute(query, (coach_name,))
    db.commit()

def update_coach(coach_id, column, new_value):
    query = f'''
    UPDATE Coach
    SET {column} = %s
    WHERE CoachID = %s'''
    cursor.execute(query, (new_value, coach_id))
    db.commit()
    

def get_coach(coach_name):
    query = '''
    SELECT * FROM Coach
    WHERE Name = %s'''
    cursor.execute(query, (coach_name,))
    return cursor.fetchall()

def get_coach_by_team(team_name):
    query = '''
    SELECT * FROM Coach
    INNER JOIN Team ON Coach.teamID = Team.teamID
    WHERE Team.Name = %s'''
    cursor.execute(query, (team_name,))
    return cursor.fetchall()


# -----------------------------
# GAME CRUD
# -----------------------------
def add_game(date, location, home_team_id, away_team_id, home_score, away_score):
    query = '''
    INSERT INTO Game (Date, Location, HomeTeamID, AwayTeamID, HomeScore, AwayScore)
    VALUES (%s, %s, %s, %s, %s, %s)'''
    cursor.execute(query, (date, location, home_team_id, away_team_id, home_score, away_score))
    db.commit()

def delete_game(game_id):
    query = '''
    DELETE FROM Game
    WHERE GameID = %s'''
    cursor.execute(query, (game_id,))
    db.commit()

def update_game(game_id, column, new_value):
    query = '''
    UPDATE Game
    SET {column} = %s
    WHERE GameID = %s'''
    cursor.execute(query, (new_value, game_id))
    db.commit()
def get_game(game_id):
    query = '''
    SELECT * FROM Game
    WHERE GameID = %s'''
    cursor.execute(query, (game_id,))
    return cursor.fetchall()

def get_games_by_team(team_name):
    query = '''
    SELECT * FROM Game
    INNER JOIN Team AS home_team ON Game.HomeTeamId = home_team.team_id
    INNER JOIN Team AS away_team ON Game.AwayTeamId = away_team.team_id
    WHERE home_team.Name = %s OR away_team.Name = %s'''
    cursor.execute(query, (team_name, team_name))
    return cursor.fetchall()
    

def get_games_by_date(date):
    query = '''
    SELECT * FROM Game
    WHERE Date = %s'''
    cursor.execute(query, (date,))
    return cursor.fetchall()

# -----------------------------
# PLAYER STATISTICS (BOX SCORE)
# -----------------------------
def add_player_statistics(game_id, player_id, points, rebounds, assists, blocks, steals, turnovers, minutes_played, fouls):
    query = '''
    INSERT INTO PlayerStatistics (GameID, PlayerID, Points, Rebounds, Assists, Blocks, Steals, Turnovers, MinutesPlayed, Fouls)
    VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s)'''
    cursor.execute(query, (game_id, player_id, points, rebounds, assists, blocks, steals, turnovers, minutes_played, fouls))
    db.commit()
def update_player_statistics(game_id, player_id, column, new_value):
    query = f'''
    UPDATE PlayerStatistics
    SET {column} = %s
    WHERE GameID = %s AND PlayerID = %s'''
    cursor.execute(query, (new_value, game_id, player_id))
    db.commit()
    

def get_player_statistics(game_id, player_id):
    query = '''
    SELECT * FROM PlayerStatistics
    WHERE GameID = %s AND PlayerID = %s'''
    cursor.execute(query, (game_id, player_id))
    return cursor.fetchall()

def get_statistics_by_player(player_id):
    query = '''
    SELECT * FROM PlayerStatistics
    WHERE PlayerID = %s'''
    cursor.execute(query, (player_id,))
    return cursor.fetchall()

def get_statistics_by_game(game_id):
    query = '''
    SELECT * FROM PlayerStatistics
    WHERE GameID = %s'''
    cursor.execute(query, (game_id,))
    return cursor.fetchall()

def get_average_statistics_by_player(player_name):
    query = '''
    
    SELECT AVG(Points) AS AvgPoints, AVG(Rebounds) AS AvgRebounds, AVG(Assists) AS AvgAssists,
           AVG(Blocks) AS AvgBlocks, AVG(Steals) AS AvgSteals, AVG(Turnovers) AS AvgTurnovers,
           AVG(MinutesPlayed) AS AvgMinutesPlayed, AVG(Fouls) AS AvgFouls
    FROM PlayerStatistics
    INNER JOIN Player ON PlayerStatistics.PlayerID = Player.PlayerID
    WHERE Player.Name = %s'''
    cursor.execute(query, (player_name,))
    return cursor.fetchall()