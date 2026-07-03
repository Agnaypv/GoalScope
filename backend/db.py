import sqlite3
import os


# Database file path
DB_PATH = "football_stats.db"

def create_database():
    """Create all database tables for football stats explorer"""
    
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()
    
    # Drop tables if they exist (for fresh start)
    cursor.execute("DROP TABLE IF EXISTS awards")
    cursor.execute("DROP TABLE IF EXISTS league_standings")
    cursor.execute("DROP TABLE IF EXISTS fixtures")
    cursor.execute("DROP TABLE IF EXISTS players")
    
    # Create Players Table
    cursor.execute("""
        CREATE TABLE players (
            id INTEGER PRIMARY KEY,
            name TEXT NOT NULL,
            team TEXT NOT NULL,
            position TEXT NOT NULL,
            goals INTEGER,
            assists INTEGER,
            appearances INTEGER,
            nationality TEXT,
            age INTEGER,
            rating REAL,
            league TEXT NOT NULL
        )
    """)
    
    # Create Fixtures Table
    cursor.execute("""
        CREATE TABLE fixtures (
            id INTEGER PRIMARY KEY,
            home_team TEXT NOT NULL,
            away_team TEXT NOT NULL,
            match_date TEXT NOT NULL,
            result TEXT,
            league TEXT NOT NULL
        )
    """)
    
    # Create League Standings Table
    cursor.execute("""
        CREATE TABLE league_standings (
            id INTEGER PRIMARY KEY,
            league TEXT NOT NULL,
            position INTEGER,
            team TEXT NOT NULL,
            played INTEGER,
            wins INTEGER,
            draws INTEGER,
            losses INTEGER,
            goals_for INTEGER,
            goals_against INTEGER,
            points INTEGER
        )
    """)
    
    # Create Awards Table
    cursor.execute("""
        CREATE TABLE awards (
            id INTEGER PRIMARY KEY,
            award_name TEXT NOT NULL,
            player_name TEXT NOT NULL,
            season TEXT,
            league TEXT NOT NULL
        )
    """)
    
    conn.commit()
    conn.close()
    print("Database created successfully!")


def insert_players():
    """Insert sample player data into the database"""
    
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()
    
    players = [
        # Premier League
        (1, "Erling Haaland", "Manchester City", "Forward", 36, 8, 35, "Norway", 23, 8.9, "Premier League"),
        (2, "Mohamed Salah", "Liverpool", "Forward", 19, 13, 38, "Egypt", 31, 8.5, "Premier League"),
        (3, "Harry Kane", "Tottenham", "Forward", 17, 5, 37, "England", 30, 8.2, "Premier League"),
        (4, "Kevin De Bruyne", "Manchester City", "Midfielder", 8, 17, 25, "Belgium", 32, 8.7, "Premier League"),
        (5, "Bruno Fernandes", "Manchester United", "Midfielder", 8, 12, 37, "Portugal", 29, 8.3, "Premier League"),
        (6, "Bukayo Saka", "Arsenal", "Forward", 14, 5, 35, "England", 22, 8.1, "Premier League"),
        (7, "Declan Rice", "Arsenal", "Midfielder", 2, 0, 33, "England", 24, 7.9, "Premier League"),
        (8, "Virgil van Dijk", "Liverpool", "Defender", 2, 0, 30, "Netherlands", 31, 8.4, "Premier League"),
        (9, "Callum Wilson", "Newcastle", "Forward", 15, 2, 30, "England", 31, 8.0, "Premier League"),
        (10, "Phil Foden", "Manchester City", "Midfielder", 11, 6, 24, "England", 23, 8.2, "Premier League"),
        
        # La Liga
        (11, "Karim Benzema", "Real Madrid", "Forward", 26, 8, 32, "France", 35, 8.8, "La Liga"),
        (12, "Robert Lewandowski", "Barcelona", "Forward", 23, 8, 31, "Poland", 34, 8.6, "La Liga"),
        (13, "Vinícius Júnior", "Real Madrid", "Forward", 20, 6, 30, "Brazil", 22, 8.3, "La Liga"),
        (14, "Gavi", "Barcelona", "Midfielder", 5, 3, 28, "Spain", 19, 7.8, "La Liga"),
        (15, "Federico Valverde", "Real Madrid", "Midfielder", 4, 2, 29, "Uruguay", 24, 7.9, "La Liga"),
        (16, "Pedri", "Barcelona", "Midfielder", 3, 5, 25, "Spain", 20, 7.7, "La Liga"),
        (17, "Rodrygo", "Real Madrid", "Forward", 10, 4, 22, "Brazil", 21, 7.6, "La Liga"),
        (18, "Sergio Busquets", "Barcelona", "Midfielder", 1, 0, 26, "Spain", 34, 7.5, "La Liga"),
        (19, "Luka Modrić", "Real Madrid", "Midfielder", 2, 2, 29, "Croatia", 37, 8.0, "La Liga"),
        (20, "Ousmane Dembélé", "Barcelona", "Forward", 8, 5, 24, "France", 25, 7.8, "La Liga"),
        
        # Serie A
        (21, "Victor Osimhen", "Napoli", "Forward", 15, 3, 27, "Nigeria", 24, 8.1, "Serie A"),
        (22, "Dušan Vlahović", "Juventus", "Forward", 16, 6, 31, "Serbia", 23, 8.2, "Serie A"),
        (23, "Juan Cuadrado", "Juventus", "Midfielder", 4, 7, 28, "Colombia", 34, 7.7, "Serie A"),
        (24, "Khvicha Kvaratskhelia", "Napoli", "Forward", 12, 6, 25, "Georgia", 21, 8.0, "Serie A"),
        (25, "Matteo Politano", "Napoli", "Forward", 10, 4, 26, "Italy", 26, 7.8, "Serie A"),
        (26, "Fabián Ruiz", "Napoli", "Midfielder", 3, 2, 24, "Spain", 26, 7.6, "Serie A"),
        (27, "Hirving Lozano", "Napoli", "Forward", 9, 5, 23, "Mexico", 27, 7.7, "Serie A"),
        (28, "Alessandro Bastoni", "Inter", "Defender", 1, 0, 22, "Italy", 24, 7.9, "Serie A"),
        (29, "Nicolo Barella", "Inter", "Midfielder", 5, 3, 26, "Italy", 25, 7.8, "Serie A"),
        (30, "Lautaro Martínez", "Inter", "Forward", 16, 5, 29, "Argentina", 25, 8.3, "Serie A"),
        
        # Bundesliga
        (31, "Serge Gnabry", "Bayern Munich", "Forward", 14, 6, 28, "Germany", 27, 8.0, "Bundesliga"),
        (32, "Harry Kane", "Bayern Munich", "Forward", 36, 8, 39, "England", 30, 8.5, "Bundesliga"),
        (33, "Jamal Musiala", "Bayern Munich", "Forward", 11, 6, 32, "Germany", 20, 8.1, "Bundesliga"),
        (34, "Leroy Sané", "Bayern Munich", "Forward", 6, 5, 21, "Germany", 27, 7.8, "Bundesliga"),
        (35, "Thomas Müller", "Bayern Munich", "Midfielder", 5, 11, 32, "Germany", 33, 7.9, "Bundesliga"),
        (36, "Joshua Kimmich", "Bayern Munich", "Midfielder", 3, 2, 31, "Germany", 28, 7.8, "Bundesliga"),
        (37, "Jude Bellingham", "Borussia Dortmund", "Midfielder", 8, 7, 27, "England", 20, 8.2, "Bundesliga"),
        (38, "Marco Reus", "Borussia Dortmund", "Forward", 12, 7, 28, "Germany", 33, 7.9, "Bundesliga"),
        (39, "Niclas Füllkrug", "Werder Bremen", "Forward", 16, 2, 29, "Germany", 29, 8.0, "Bundesliga"),
        (40, "Florian Wirtz", "Bayer Leverkusen", "Forward", 11, 7, 23, "Germany", 20, 8.1, "Bundesliga"),
        
        # Ligue 1
        (41, "Kylian Mbappé", "Paris Saint-Germain", "Forward", 29, 12, 31, "France", 24, 8.8, "Ligue 1"),
        (42, "Neymar Jr", "Paris Saint-Germain", "Forward", 8, 11, 23, "Brazil", 31, 8.2, "Ligue 1"),
        (43, "Lionel Messi", "Paris Saint-Germain", "Forward", 11, 15, 28, "Argentina", 35, 8.5, "Ligue 1"),
        (44, "Achraf Hakimi", "Paris Saint-Germain", "Midfielder", 6, 10, 32, "Morocco", 24, 8.1, "Ligue 1"),
        (45, "Marco Verratti", "Paris Saint-Germain", "Midfielder", 1, 1, 25, "Italy", 30, 7.8, "Ligue 1"),
        (46, "Alexandre Lacazette", "Lyon", "Forward", 19, 5, 31, "France", 32, 8.0, "Ligue 1"),
        (47, "Moussa Dembélé", "Lyon", "Forward", 12, 2, 28, "France", 28, 7.7, "Ligue 1"),
        (48, "Jonathan Clauss", "Lens", "Midfielder", 4, 7, 29, "France", 30, 7.6, "Ligue 1"),
        (49, "Seko Fofana", "Lens", "Midfielder", 3, 1, 27, "Ivory Coast", 27, 7.5, "Ligue 1"),
        (50, "Danilo Pereira", "Paris Saint-Germain", "Defender", 1, 0, 24, "Portugal", 28, 7.7, "Ligue 1"),
    ]
    
    for player in players:
        cursor.execute("""
            INSERT INTO players (id, name, team, position, goals, assists, appearances, nationality, age, rating, league)
            VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
        """, player)
    
    conn.commit()
    conn.close()
    print("Players data inserted!")


def insert_fixtures():
    """Insert sample fixture data"""
    
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()
    
    fixtures = [
        # Premier League
        (1, "Manchester City", "Liverpool", "2024-01-15", "2-1", "Premier League"),
        (2, "Arsenal", "Tottenham", "2024-01-16", "3-2", "Premier League"),
        (3, "Manchester United", "Chelsea", "2024-01-17", "1-1", "Premier League"),
        (4, "Newcastle", "Brighton", "2024-01-18", "2-0", "Premier League"),
        (5, "Aston Villa", "Everton", "2024-01-19", "3-1", "Premier League"),
        (6, "West Ham", "Fulham", "2024-01-20", "1-2", "Premier League"),
        (7, "Brentford", "Luton", "2024-01-21", "2-2", "Premier League"),
        (8, "Bournemouth", "Crystal Palace", "2024-01-22", "1-0", "Premier League"),
        (9, "Nottingham Forest", "Leicester", "2024-01-23", "0-0", "Premier League"),
        (10, "Wolverhampton", "Southampton", "2024-01-24", "2-1", "Premier League"),
        
        # La Liga
        (11, "Real Madrid", "Barcelona", "2024-01-15", "3-1", "La Liga"),
        (12, "Atletico Madrid", "Sevilla", "2024-01-16", "2-0", "La Liga"),
        (13, "Valencia", "Real Sociedad", "2024-01-17", "1-2", "La Liga"),
        (14, "Villarreal", "Osasuna", "2024-01-18", "2-1", "La Liga"),
        (15, "Getafe", "Celta Vigo", "2024-01-19", "0-1", "La Liga"),
        (16, "Rayo Vallecano", "Almeria", "2024-01-20", "1-1", "La Liga"),
        (17, "Real Betis", "Girona", "2024-01-21", "2-2", "La Liga"),
        (18, "Cadiz", "Las Palmas", "2024-01-22", "0-0", "La Liga"),
        (19, "Bilbao", "Malaga", "2024-01-23", "3-0", "La Liga"),
        (20, "Alaves", "Vallecano", "2024-01-24", "1-2", "La Liga"),
        
        # Serie A
        (21, "Napoli", "Juventus", "2024-01-15", "2-1", "Serie A"),
        (22, "Inter", "AC Milan", "2024-01-16", "1-1", "Serie A"),
        (23, "Roma", "Lazio", "2024-01-17", "2-0", "Serie A"),
        (24, "Fiorentina", "Atalanta", "2024-01-18", "1-3", "Serie A"),
        (25, "Torino", "Bologna", "2024-01-19", "2-2", "Serie A"),
        (26, "Sampdoria", "Sassuolo", "2024-01-20", "0-1", "Serie A"),
        (27, "Venezia", "Frosinone", "2024-01-21", "1-2", "Serie A"),
        (28, "Empoli", "Como", "2024-01-22", "2-1", "Serie A"),
        (29, "Spezia", "Verona", "2024-01-23", "1-1", "Serie A"),
        (30, "Lecce", "Monza", "2024-01-24", "0-0", "Serie A"),
        
        # Bundesliga
        (31, "Bayern Munich", "Dortmund", "2024-01-15", "3-0", "Bundesliga"),
        (32, "Leverkusen", "Leipzig", "2024-01-16", "2-1", "Bundesliga"),
        (33, "Stuttgart", "Hoffenheim", "2024-01-17", "1-2", "Bundesliga"),
        (34, "Frankfurt", "Wolfsburg", "2024-01-18", "2-2", "Bundesliga"),
        (35, "Cologne", "Mainz", "2024-01-19", "0-1", "Bundesliga"),
        (36, "Union Berlin", "Freiburg", "2024-01-20", "1-0", "Bundesliga"),
        (37, "Augsburg", "Bochum", "2024-01-21", "2-1", "Bundesliga"),
        (38, "Eintracht Frankfurt", "Hertha", "2024-01-22", "3-0", "Bundesliga"),
        (39, "Werder Bremen", "Fortuna", "2024-01-23", "2-0", "Bundesliga"),
        (40, "Schalke", "Heidenheim", "2024-01-24", "0-0", "Bundesliga"),
        
        # Ligue 1
        (41, "Paris Saint-Germain", "Marseille", "2024-01-15", "4-0", "Ligue 1"),
        (42, "Monaco", "Nice", "2024-01-16", "2-1", "Ligue 1"),
        (43, "Lyon", "Lille", "2024-01-17", "1-2", "Ligue 1"),
        (44, "Lens", "Rennes", "2024-01-18", "2-2", "Ligue 1"),
        (45, "Toulouse", "Nantes", "2024-01-19", "1-0", "Ligue 1"),
        (46, "Strasbourg", "Montpellier", "2024-01-20", "3-1", "Ligue 1"),
        (47, "Angers", "Lorient", "2024-01-21", "1-1", "Ligue 1"),
        (48, "Auxerre", "Clermont", "2024-01-22", "2-1", "Ligue 1"),
        (49, "Le Havre", "Reims", "2024-01-23", "0-1", "Ligue 1"),
        (50, "Troyes", "Ajaccio", "2024-01-24", "1-0", "Ligue 1"),
    ]
    
    for fixture in fixtures:
        cursor.execute("""
            INSERT INTO fixtures (id, home_team, away_team, match_date, result, league)
            VALUES (?, ?, ?, ?, ?, ?)
        """, fixture)
    
    conn.commit()
    conn.close()
    print("Fixtures data inserted!")


def insert_league_standings():
    """Insert league standings data"""
    
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()
    
    standings = [
        # Premier League
        (1, "Premier League", 1, "Manchester City", 20, 15, 3, 2, 45, 15, 48),
        (2, "Premier League", 2, "Arsenal", 20, 14, 4, 2, 48, 18, 46),
        (3, "Premier League", 3, "Liverpool", 20, 12, 5, 3, 42, 22, 41),
        (4, "Premier League", 4, "Tottenham", 20, 11, 4, 5, 38, 28, 37),
        (5, "Premier League", 5, "Newcastle", 20, 10, 3, 7, 35, 26, 33),
        
        # La Liga
        (6, "La Liga", 1, "Real Madrid", 20, 16, 2, 2, 52, 18, 50),
        (7, "La Liga", 2, "Barcelona", 20, 14, 3, 3, 48, 22, 45),
        (8, "La Liga", 3, "Atletico Madrid", 20, 12, 4, 4, 40, 25, 40),
        (9, "La Liga", 4, "Real Sociedad", 20, 11, 3, 6, 38, 28, 36),
        (10, "La Liga", 5, "Valencia", 20, 10, 2, 8, 35, 32, 32),
        
        # Serie A
        (11, "Serie A", 1, "Napoli", 20, 16, 2, 2, 52, 18, 50),
        (12, "Serie A", 2, "Juventus", 20, 14, 3, 3, 45, 22, 45),
        (13, "Serie A", 3, "Inter", 20, 13, 2, 5, 42, 28, 41),
        (14, "Serie A", 4, "Roma", 20, 12, 1, 7, 40, 32, 37),
        (15, "Serie A", 5, "Lazio", 20, 11, 2, 7, 38, 35, 35),
        
        # Bundesliga
        (16, "Bundesliga", 1, "Bayern Munich", 20, 16, 2, 2, 52, 18, 50),
        (17, "Bundesliga", 2, "Borussia Dortmund", 20, 14, 2, 4, 48, 25, 44),
        (18, "Bundesliga", 3, "Bayer Leverkusen", 20, 12, 3, 5, 42, 30, 39),
        (19, "Bundesliga", 4, "Stuttgart", 20, 11, 2, 7, 40, 32, 35),
        (20, "Bundesliga", 5, "Leipzig", 20, 10, 2, 8, 38, 35, 32),
        
        # Ligue 1
        (21, "Ligue 1", 1, "Paris Saint-Germain", 20, 16, 2, 2, 55, 18, 50),
        (22, "Ligue 1", 2, "Monaco", 20, 13, 2, 5, 45, 28, 41),
        (23, "Ligue 1", 3, "Lens", 20, 12, 3, 5, 42, 32, 39),
        (24, "Ligue 1", 4, "Lyon", 20, 11, 2, 7, 40, 35, 35),
        (25, "Ligue 1", 5, "Lille", 20, 10, 2, 8, 38, 38, 32),
    ]
    
    for standing in standings:
        cursor.execute("""
            INSERT INTO league_standings (id, league, position, team, played, wins, draws, losses, goals_for, goals_against, points)
            VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
        """, standing)
    
    conn.commit()
    conn.close()
    print("League standings data inserted!")


def insert_awards():
    """Insert awards and achievements data"""
    
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()
    
    awards = [
        (1, "Top Scorer", "Erling Haaland", "2023-24", "Premier League"),
        (2, "Top Scorer", "Karim Benzema", "2023-24", "La Liga"),
        (3, "Top Scorer", "Victor Osimhen", "2023-24", "Serie A"),
        (4, "Top Scorer", "Harry Kane", "2023-24", "Bundesliga"),
        (5, "Top Scorer", "Kylian Mbappé", "2023-24", "Ligue 1"),
        (6, "Top Assist", "Kevin De Bruyne", "2023-24", "Premier League"),
        (7, "Top Assist", "Federico Valverde", "2023-24", "La Liga"),
        (8, "Top Assist", "Thomas Müller", "2023-24", "Bundesliga"),
        (9, "Top Assist", "Neymar Jr", "2023-24", "Ligue 1"),
        (10, "Player of Month", "Mohamed Salah", "December 2023", "Premier League"),
        (11, "Player of Month", "Vinícius Júnior", "December 2023", "La Liga"),
        (12, "Player of Month", "Khvicha Kvaratskhelia", "December 2023", "Serie A"),
        (13, "Player of Month", "Jamal Musiala", "December 2023", "Bundesliga"),
        (14, "Player of Month", "Kylian Mbappé", "December 2023", "Ligue 1"),
        (15, "Golden Boot", "Erling Haaland", "2023", "International"),
        (16, "Best Defender", "Virgil van Dijk", "2023", "Premier League"),
        (17, "Best Goalkeeper", "Ederson", "2023", "Premier League"),
        (18, "Best Midfielder", "Kevin De Bruyne", "2023", "Premier League"),
        (19, "100+ Goals Club", "Karim Benzema", "Career", "La Liga"),
        (20, "50+ Assists", "Kevin De Bruyne", "Career", "Premier League"),
    ]
    
    for award in awards:
        cursor.execute("""
            INSERT INTO awards (id, award_name, player_name, season, league)
            VALUES (?, ?, ?, ?, ?)
        """, award)
    
    conn.commit()
    conn.close()
    print("Awards data inserted!")


def get_all_players():
    """Get all players from database"""
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM players")
    players = cursor.fetchall()
    conn.close()
    return players


def search_player(name):
    """Search for a player by name"""
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM players WHERE name LIKE ?", (f"%{name}%",))
    player = cursor.fetchall()
    conn.close()
    return player


def get_league_table(league):
    """Get league standings for a specific league"""
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM league_standings WHERE league = ? ORDER BY position", (league,))
    standings = cursor.fetchall()
    conn.close()
    return standings


def get_fixtures():
    """Get all upcoming and recent fixtures"""
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM fixtures ORDER BY match_date")
    fixtures = cursor.fetchall()
    conn.close()
    return fixtures


def get_top_scorers(league=None):
    """Get top scorers, optionally filtered by league"""
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()
    
    if league:
        cursor.execute("""
            SELECT name, team, goals, league FROM players 
            WHERE league = ? 
            ORDER BY goals DESC 
            LIMIT 10
        """, (league,))
    else:
        cursor.execute("""
            SELECT name, team, goals, league FROM players 
            ORDER BY goals DESC 
            LIMIT 10
        """)
    
    scorers = cursor.fetchall()
    conn.close()
    return scorers


def get_top_assisters(league=None):
    """Get top assist makers, optionally filtered by league"""
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()
    
    if league:
        cursor.execute("""
            SELECT name, team, assists, league FROM players 
            WHERE league = ? 
            ORDER BY assists DESC 
            LIMIT 10
        """, (league,))
    else:
        cursor.execute("""
            SELECT name, team, assists, league FROM players 
            ORDER BY assists DESC 
            LIMIT 10
        """)
    
    assisters = cursor.fetchall()
    conn.close()
    return assisters


def get_awards(award_name=None):
    """Get awards, optionally filtered by award type"""
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()
    
    if award_name:
        cursor.execute("SELECT * FROM awards WHERE award_name = ?", (award_name,))
    else:
        cursor.execute("SELECT * FROM awards")
    
    awards = cursor.fetchall()
    conn.close()
    return awards


def get_all_leagues():
    """Get all leagues in database"""
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()
    cursor.execute("SELECT DISTINCT league FROM players ORDER BY league")
    leagues = cursor.fetchall()
    conn.close()
    return [league[0] for league in leagues]


# Initialize database on import
if __name__ == "__main__":
    create_database()
    insert_players()
    insert_fixtures()
    insert_league_standings()
    insert_awards()
    print("\nDatabase setup complete!")


