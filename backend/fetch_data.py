import requests
import os

API_KEY = os.getenv("API_KEY")

HEADERS = {
    "X-RapidAPI-Key": API_KEY,
    "X-RapidAPI-Host": "v3.football.api-sports.io"
}

# Base URL
BASE_URL = "https://v3.football.api-sports.io"



LEAGUES = {
    "Premier League": 39,      # EPL
    "La Liga": 140,            # Spain
    "Serie A": 135,            # Italy
    "Bundesliga": 78,          # Germany
    "Ligue 1": 61              # France
}

SEASON = 2024


def fetch_players():
    """Fetch top players from all leagues"""
    print("Fetching players from API...")
    
    all_players = []
    
    for league_name, league_id in LEAGUES.items():
        try:
            print(f"  Fetching {league_name}...")
            
            url = f"{BASE_URL}/players/topscorers"
            params = {
                "league": league_id,
                "season": SEASON
            }
            
            response = requests.get(url, headers=HEADERS, params=params)
            
            if response.status_code == 200:
                data = response.json()
                
                for item in data.get('response', [])[:10]:
                    try:
                        player = item.get('player', {})
                        stats = item.get('statistics', [{}])[0]
                        
                        player_data = {
                            'name': player.get('name', 'Unknown'),
                            'team': stats.get('team', {}).get('name', 'Unknown'),
                            'position': stats.get('games', {}).get('position', 'Unknown'),
                            'goals': stats.get('goals', {}).get('total', 0),
                            'assists': stats.get('goals', {}).get('assists', 0),
                            'appearances': stats.get('games', {}).get('appearences', 0),
                            'nationality': player.get('nationality', 'Unknown'),
                            'age': player.get('age', 0),
                            'rating': float(stats.get('games', {}).get('rating', 7.0)) if stats.get('games', {}).get('rating') else 7.0,
                            'league': league_name
                        }
                        
                        all_players.append(player_data)
                    except Exception as e:
                        print(f"    Error parsing player: {e}")
                        continue
            else:
                print(f"  Error fetching {league_name}: {response.status_code}")
        
        except Exception as e:
            print(f"  Error: {e}")
            continue
    
    print(f"✅ Fetched {len(all_players)} players")
    return all_players


def fetch_fixtures():
    """Fetch recent and upcoming fixtures"""
    print("Fetching fixtures from API...")
    
    all_fixtures = []
    
    for league_name, league_id in LEAGUES.items():
        try:
            print(f"  Fetching fixtures for {league_name}...")
            
            url = f"{BASE_URL}/fixtures"
            params = {
                "league": league_id,
                "season": SEASON,
                "last": 5
            }
            
            response = requests.get(url, headers=HEADERS, params=params)
            
            if response.status_code == 200:
                data = response.json()
                
                for fixture in data.get('response', []):
                    try:
                        home_team = fixture.get('teams', {}).get('home', {}).get('name', 'Unknown')
                        away_team = fixture.get('teams', {}).get('away', {}).get('name', 'Unknown')
                        fixture_date = fixture.get('fixture', {}).get('date', 'Unknown')
                        
                        goals = fixture.get('goals', {})
                        home_goals = goals.get('home', 0)
                        away_goals = goals.get('away', 0)
                        
                        if home_goals is not None and away_goals is not None:
                            result = f"{home_goals}-{away_goals}"
                        else:
                            result = "vs"
                        
                        fixture_data = {
                            'home_team': home_team,
                            'away_team': away_team,
                            'match_date': fixture_date,
                            'result': result,
                            'league': league_name
                        }
                        
                        all_fixtures.append(fixture_data)
                    except Exception as e:
                        print(f"    Error parsing fixture: {e}")
                        continue
            else:
                print(f"  Error: {response.status_code}")
        
        except Exception as e:
            print(f"  Error: {e}")
            continue
    
    print(f"✅ Fetched {len(all_fixtures)} fixtures")
    return all_fixtures


def fetch_standings():
    """Fetch league standings"""
    print("Fetching standings from API...")
    
    all_standings = []
    
    for league_name, league_id in LEAGUES.items():
        try:
            print(f"  Fetching standings for {league_name}...")
            
            url = f"{BASE_URL}/standings"
            params = {
                "league": league_id,
                "season": SEASON
            }
            
            response = requests.get(url, headers=HEADERS, params=params)
            
            if response.status_code == 200:
                data = response.json()
                
                for group in data.get('response', []):
                    standings_list = group.get('league', {}).get('standings', [[]])[0]
                    
                    for standing in standings_list[:5]:
                        try:
                            standing_data = {
                                'league': league_name,
                                'position': standing.get('rank', 0),
                                'team': standing.get('team', {}).get('name', 'Unknown'),
                                'played': standing.get('all', {}).get('played', 0),
                                'wins': standing.get('all', {}).get('win', 0),
                                'draws': standing.get('all', {}).get('draw', 0),
                                'losses': standing.get('all', {}).get('lose', 0),
                                'goals_for': standing.get('all', {}).get('goals', {}).get('for', 0),
                                'goals_against': standing.get('all', {}).get('goals', {}).get('against', 0),
                                'points': standing.get('points', 0)
                            }
                            
                            all_standings.append(standing_data)
                        except Exception as e:
                            print(f"    Error parsing standing: {e}")
                            continue
            else:
                print(f"  Error: {response.status_code}")
        
        except Exception as e:
            print(f"  Error: {e}")
            continue
    
    print(f"✅ Fetched {len(all_standings)} standings")
    return all_standings


def fetch_awards():
    """Fetch awards"""
    print("Fetching awards from API...")
    
    all_awards = []
    
    for league_name, league_id in LEAGUES.items():
        try:
            print(f"  Fetching awards for {league_name}...")
            
            url = f"{BASE_URL}/players/topscorers"
            params = {
                "league": league_id,
                "season": SEASON
            }
            
            response = requests.get(url, headers=HEADERS, params=params)
            
            if response.status_code == 200:
                data = response.json()
                
                top_scorers = data.get('response', [])[:3]
                
                for rank, item in enumerate(top_scorers, 1):
                    player_name = item.get('player', {}).get('name', 'Unknown')
                    goals = item.get('statistics', [{}])[0].get('goals', {}).get('total', 0)
                    
                    award_data = {
                        'award_name': 'Top Scorer',
                        'player_name': player_name,
                        'season': str(SEASON),
                        'league': league_name
                    }
                    
                    all_awards.append(award_data)
        
        except Exception as e:
            print(f"  Error: {e}")
            continue
    
    print(f"✅ Fetched {len(all_awards)} awards")
    return all_awards


if __name__ == "__main__":
    print("=" * 60)
    print("FETCHING REAL DATA FROM API-FOOTBALL.COM")
    print("=" * 60)
    
    print("\nTesting API connection...")
    try:
        test_url = f"{BASE_URL}/players/topscorers"
        test_params = {"league": 39, "season": 2024}
        test_response = requests.get(test_url, headers=HEADERS, params=test_params)
        
        if test_response.status_code == 200:
            print("✅ API connection successful!")
        else:
            print(f"❌ API error: {test_response.status_code}")
            print("Make sure your API key is correct!")
            exit(1)
    except Exception as e:
        print(f"❌ Error connecting to API: {e}")
        exit(1)
    
    print("\n" + "=" * 60)
    players = fetch_players()
    print("\n" + "=" * 60)
    fixtures = fetch_fixtures()
    print("\n" + "=" * 60)
    standings = fetch_standings()
    print("\n" + "=" * 60)
    awards = fetch_awards()
    
    print("\n" + "=" * 60)
    print("SUMMARY")
    print("=" * 60)
    print(f"Players: {len(players)}")
    print(f"Fixtures: {len(fixtures)}")
    print(f"Standings: {len(standings)}")
    print(f"Awards: {len(awards)}")
    print("=" * 60)
    
    if players:
        print("\nSample Players:")
        for p in players[:3]:
            print(f"  {p['name']} - {p['team']} - {p['goals']} goals")
    
    print("\n✅ All data fetched successfully!")
    print("Next: Run update_database.py to update your database")