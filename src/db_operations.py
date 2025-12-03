import mysql.connector
from helper import helper

class db_operations():

    def __init__(self):
        # Make connection
        self.connection = mysql.connector.connect(host="localhost",
            user= "root",
            password= "CPSC408!",
            auth_plugin= 'mysql_native_password',
            database = "NBA")
        print("Connection made...")
        self.cursor = self.connection.cursor()
        print("Cursor object made...")

#=============================================================
# FUNCTIONS FOR CREATING TABLES AND POPULATING
    def create_team(self):
        query = '''
        CREATE TABLE Team (
            TeamID INT PRIMARY KEY AUTO_INCREMENT,
            Name VARCHAR(70),
            City VARCHAR(70),
            Division VARCHAR(30),
            Conference VARCHAR(30),
        );
        '''
        self.cursor.execute(query)
        print('Team Table Created')

    def create_coach(self):
        query = '''
        CREATE TABLE Coach (
            CoachID INT PRIMARY KEY AUTO_INCREMENT,
            Name VARCHAR(80),
            Salary INT,
            TeamID INT
        );
        '''
        self.cursor.execute(query)
        print('Coach Table Created')

    def create_player(self):
        query = '''
        CREATE TABLE Player (
            PlayerID INT PRIMARY KEY AUTO_INCREMENT,
            Name VARCHAR(70),
            Height INT,
            Weight INT,
            Age INT,
            Position VARCHAR(2),
            TeamID INT
        );
        '''
        self.cursor.execute(query)
        print('Player Table Created')

    def create_game(self):
        query = '''
        CREATE TABLE Game (
            GameID INT PRIMARY KEY AUTO_INCREMENT,
            Date DATE,
            Location VARCHAR(80),
            HomeTeamID INT,
            AwayTeamID INT,
            HomeScore INT,
            AwayScore INT
        );
        '''
        self.cursor.execute(query)
        print('Game Table Created')        

    def create_playergamestatistics(self):
        query = '''
        CREATE TABLE PlayerGameStatistics (
            GameID INT,
            PlayerID INT,
            Points INT,
            Rebounds INT,
            Assists INT,
            Blocks INT,
            Steals INT,
            Turnovers INT,
            MinutesPlayed INT,
            Fouls INT,
            PRIMARY KEY (GameID, PlayerID),
            FOREIGN KEY (GameID) REFERENCES Game(GameID),
            FOREIGN KEY (PlayerID) REFERENCES Player(PlayerID)
        );
        '''
        self.cursor.execute(query)
        print('PlayerGameStatistics Table Created')   

    def update_fk_tables(self):
        query = '''
        ALTER TABLE Coach
        ADD CONSTRAINT fk_coach_team
        FOREIGN KEY (TeamID) REFERENCES Team(TeamID);

        ALTER TABLE Player
        ADD CONSTRAINT fk_player_team
        FOREIGN KEY (TeamID) REFERENCES Team(TeamID);

        ALTER TABLE Game
        ADD CONSTRAINT fk_home_game_team
        FOREIGN KEY (HomeTeamID) REFERENCES Team(TeamID),
        ADD CONSTRAINT fk_away_game_team
        FOREIGN KEY (AwayTeamID) REFERENCES Team(TeamID);
        '''
        self.cursor.execute(query)
        print('Foreign Keys Updated')    

    def create_all_tables(self):
        self.create_team()
        self.create_coach()
        self.create_player()
        self.create_game()
        self.create_playergamestatistics()
        self.update_fk_tables()

    #incase tables are messed up and need to be deleted and readded
    def reset(self):
        query = '''
        DROP TABLE Team;
        DROP TABLE Coach;
        DROP TABLE Player;
        DROP TABLE Game;
        DROP TABLE PlayerGameStatistics;
        '''
        self.cursor.execute(query)
        print('All tables deleted')

    def populate_table(self, table, filepath, values):
        data = helper.data_cleaner(filepath)
        attribute_count = len(data[0])
        placeholders = ("%s,"*attribute_count)[:-1]
        query = f"INSERT INTO {table} ({values}) VALUES("+placeholders+")"
        self.bulk_insert(query, data)
        print(f"Populated {table}")

#=============================================================



# -----------------------------
# REPORTS & SPECIAL QUERIES
# -----------------------------
    def get_top_players_by_avg_points(self):
        query = f'''
        SELECT
            Player.PlayerID,
            Player.Name,
            AVG(PlayerGameStatistics.Points) AS avg_points
        FROM Player
        JOIN PlayerGameStatistics ON Player.PlayerID = PlayerGameStatistics.PlayerID
        GROUP BY Player.PlayerID, Player.name
        ORDER BY avg_points DESC
        LIMIT 10;
        '''
        result = self.select_query(query)
        return helper.pretty_print(result)

    def get_top_players_by_avg_assists(self):
        query = f'''
        SELECT
            Player.PlayerID,
            Player.Name,
            AVG(PlayerGameStatistics.Assists) AS avg_assists
        FROM Player
        INNER JOIN PlayerGameStatistics ON Player.PlayerID = PlayerGameStatistics.PlayerID
        GROUP BY Player.PlayerID, Player.name
        ORDER BY avg_assists DESC
        LIMIT 10;
        '''
        result = self.select_query(query)
        return helper.pretty_print(result)

    def get_top_players_by_avg_rebounds(self):
        query = f'''
        SELECT
            Player.PlayerID,
            Player.Name,
            AVG(PlayerGameStatistics.Rebounds) AS avg_rebounds
        FROM Player
        INNER JOIN PlayerGameStatistics ON Player.PlayerID = PlayerGameStatistics.PlayerID
        GROUP BY Player.PlayerID, Player.name
        ORDER BY avg_rebounds DESC
        LIMIT 10;
        '''
        result = self.select_query(query)
        return helper.pretty_print(result)

    def get_team_roster(self, team_name):
        query = '''
        SELECT PlayerID, Player.Name, Position, Player.Age
        FROM Player
        INNER JOIN Team ON Player.TeamID = Team.TeamID
        WHERE Team.name = %s
        '''
        record = (team_name,)
        result = self.select_query_params(query, record)
        return helper.pretty_print(result)



    def search_player_by_name(self, name):
        query = '''
        SELECT *
        FROM Player
        WHERE Player.name = %s
        '''
        record = (name,)
        result = self.select_query_params(query, record)
        return helper.pretty_print(result)

#=============================================================




# -----------------------------
# TRADE OPERATIONS
# -----------------------------

    def get_player_id(self, name):
        query = '''
        SELECT PlayerID
        FROM Player
        WHERE name = %s;
        '''
        record = (name,)
        result = self.select_query_params(query, record)
        return result[0][0]
     
        
    def get_team_id(self, name):
        query = '''
        SELECT TeamID
        FROM Team
        WHERE name = %s;
        '''
        record = (name,)
        result = self.select_query_params(query, record)
        return result[0][0]
    
    def trade_player(self, playername, newteamname):
        player_id = self.get_player_id(playername)
        team_id = self.get_team_id(newteamname)
        query = '''
        UPDATE Player
        SET TeamID = %s
        WHERE PlayerID = %s;
        '''
        record = (team_id, player_id)
        self.modify_query_params(query, record)
        print("Traded Player: " + playername)

    #Takes in list of players
    def trade_multiple_players(self, playernames, newteamname):
        team_id = self.get_team_id(newteamname)
        if team_id is None:
            print(f"Error: Team '{newteamname}' not found.")
            return
        query = '''
            UPDATE Player
            SET TeamID = %s
            WHERE PlayerID = %s;
        '''
        for playername in playernames:
            player_id = self.get_player_id(playername)
            if player_id is None:
                print(f"Error: Player '{playername}' not found. Skipping.")
                continue
            record = (team_id, player_id)
            self.modify_query_params(query, record)
            print("Traded Player: " + playername)
#=============================================================





    #-----------------------
    # ASSIGNMENT 4 CODE
    #------------------------

    # function to simply execute a DDL or DML query.
    # commits query, returns no results. 
    # best used for insert/update/delete queries with no parameters
    def modify_query(self, query):
        self.cursor.execute(query)
        self.connection.commit()

    # function to simply execute a DDL or DML query with parameters
    # commits query, returns no results. 
    # best used for insert/update/delete queries with named placeholders
    def modify_query_params(self, query, dictionary):
        self.cursor.execute(query, dictionary)
        self.connection.commit()

    # function to simply execute a DQL query
    # does not commit, returns results
    # best used for select queries with no parameters
    # slight edit for mysql
    def select_query(self, query):
        self.cursor.execute(query)
        result = self.cursor.fetchall()
        return result
    
    # function to simply execute a DQL query with parameters
    # does not commit, returns results
    # best used for select queries with named placeholders
    # slight edit for mysql
    def select_query_params(self, query, dictionary):
        self.cursor.execute(query, dictionary)
        result = self.cursor.fetchall()     
        return result
    
    # function to return the value of the first row's 
    # first attribute of some select query.
    # best used for querying a single aggregate select 
    # query with no parameters
    # slight edit for mysql
    def single_record(self, query):
        self.cursor.execute(query)
        return self.cursor.fetchone()[0]
    
    # function to return the value of the first row's 
    # first attribute of some select query.
    # best used for querying a single aggregate select 
    # query with named placeholders
    def single_record_params(self, query, dictionary):
        self.cursor.execute(query, dictionary)
        return self.cursor.fetchone()[0]
    
    # function to return a single attribute for all records 
    # from some table.
    # best used for select statements with no parameters
    def single_attribute(self, query):
        self.cursor.execute(query)
        results = self.cursor.fetchall()
        results = [i[0] for i in results]
        results.remove(None)
        return results
    
    # function to return a single attribute for all records 
    # from some table.
    # best used for select statements with named placeholders
    def single_attribute_params(self, query, dictionary):
        self.cursor.execute(query,dictionary)
        results = self.cursor.fetchall()
        results = [i[0] for i in results]
        return results
    
    # function for bulk inserting records
    # best used for inserting many records with parameters
    def bulk_insert(self, query, data):
        self.cursor.executemany(query, data)
        self.connection.commit()
    
    #-------------------------------
    #END OF ASSIGNMENT 4 CODE
    #-------------------------------

    def destructor(self):
        self.cursor.close()
        self.connection.close()