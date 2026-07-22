from db import create_database
from fetch_data import fetch_players, fetch_fixtures, fetch_standings, fetch_awards
import sqlite3

def update_database():
    """Update database with real API data"""
    
    print("=" * 60)
    print("UPDATING DATABASE WITH REAL DATA")
    print("=" * 60)
    
    # Step 1: Create fresh database
    print("\nStep 1: Creating database...")
    create_database()
    
    # Step 2: Fetch real data
    print("\nStep 2: Fetching real data from API...")
    players = fetch_players()
    fixtures = fetch_fixtures()
    standings = fetch_standings()
    awards = fetch_awards()
    
    # Step 3: Insert players
    print("\nStep 3: Inserting players...")
    conn = sqlite3.connect('football_stats.db')
    cursor = conn.cursor()
    
    for i, player in enumerate(players, 1):
        try:
            cursor.execute("""
                INSERT INTO players (id, name, team, position, goals, assists, appearances, nationality, age, rating, league)
                VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
            """, (
                i,
                player['name'],
                player['team'],
                player['position'],
                player['goals'],
                player['assists'],
                player['appearances'],
                player['nationality'],
                player['age'],
                player['rating'],
                player['league']
            ))
        except Exception as e:
            print(f"Error inserting player: {e}")
    
    conn.commit()
    print(f"✅ Inserted {len(players)} players")
    
    # Step 4: Insert fixtures
    print("\nStep 4: Inserting fixtures...")
    for i, fixture in enumerate(fixtures, 1):
        try:
            cursor.execute("""
                INSERT INTO fixtures (id, home_team, away_team, match_date, result, league)
                VALUES (?, ?, ?, ?, ?, ?)
            """, (
                i,
                fixture['home_team'],
                fixture['away_team'],
                fixture['match_date'],
                fixture['result'],
                fixture['league']
            ))
        except Exception as e:
            print(f"Error inserting fixture: {e}")
    
    conn.commit()
    print(f"✅ Inserted {len(fixtures)} fixtures")
    
    # Step 5: Insert standings
    print("\nStep 5: Inserting standings...")
    for i, standing in enumerate(standings, 1):
        try:
            cursor.execute("""
                INSERT INTO league_standings (id, league, position, team, played, wins, draws, losses, goals_for, goals_against, points)
                VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
            """, (
                i,
                standing['league'],
                standing['position'],
                standing['team'],
                standing['played'],
                standing['wins'],
                standing['draws'],
                standing['losses'],
                standing['goals_for'],
                standing['goals_against'],
                standing['points']
            ))
        except Exception as e:
            print(f"Error inserting standing: {e}")
    
    conn.commit()
    print(f"✅ Inserted {len(standings)} standings")
    
    # Step 6: Insert awards
    print("\nStep 6: Inserting awards...")
    for i, award in enumerate(awards, 1):
        try:
            cursor.execute("""
                INSERT INTO awards (id, award_name, player_name, season, league)
                VALUES (?, ?, ?, ?, ?)
            """, (
                i,
                award['award_name'],
                award['player_name'],
                award['season'],
                award['league']
            ))
        except Exception as e:
            print(f"Error inserting award: {e}")
    
    conn.commit()
    print(f"✅ Inserted {len(awards)} awards")
    
    conn.close()
    
    print("\n" + "=" * 60)
    print("✅ DATABASE UPDATED WITH REAL DATA!")
    print("=" * 60)
    print("\nYour database now contains:")
    print(f"  • {len(players)} real players")
    print(f"  • {len(fixtures)} real matches")
    print(f"  • {len(standings)} league standings")
    print(f"  • {len(awards)} awards")
    print("\nYour Streamlit app will now show REAL data!")
    print("\nRun: streamlit run app.py")


if __name__ == "__main__":
    update_database()