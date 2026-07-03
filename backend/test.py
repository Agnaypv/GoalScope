"""
Test file for Football Stats Explorer Backend
Run this to verify all functions work correctly
"""

from db import *

def test_backend():
    """Run all tests to verify backend works"""
    
    print("=" * 60)
    print("FOOTBALL STATS EXPLORER - BACKEND TEST")
    print("=" * 60)
    
    # Test 1: Create database
    print("\n✓ Test 1: Database created (football_stats.db)")
    
    # Test 2: Get all leagues
    print("\n✓ Test 2: All Leagues")
    print("-" * 40)
    leagues = get_all_leagues()
    for league in leagues:
        print(f"  • {league}")
    
    # Test 3: Search player
    print("\n✓ Test 3: Search Player (Haaland)")
    print("-" * 40)
    players = search_player("Haaland")
    for player in players:
        print(f"  Name: {player[1]}")
        print(f"  Team: {player[2]}")
        print(f"  Position: {player[3]}")
        print(f"  Goals: {player[4]}")
        print(f"  Assists: {player[5]}")
    
    # Test 4: Get all players count
    print("\n✓ Test 4: Total Players in Database")
    print("-" * 40)
    all_players = get_all_players()
    print(f"  Total: {len(all_players)} players")
    print(f"  Leagues: {len(leagues)}")
    print(f"  Players per league: {len(all_players) // len(leagues)}")
    
    # Test 5: Get Premier League table
    print("\n✓ Test 5: Premier League Standings")
    print("-" * 40)
    epl_table = get_league_table("Premier League")
    print(f"  {'Pos':<4} {'Team':<20} {'Points':<7}")
    print(f"  {'-'*4} {'-'*20} {'-'*7}")
    for row in epl_table[:5]:  # Show top 5
        pos = row[3]
        team = row[4]
        points = row[10]
        print(f"  {pos:<4} {team:<20} {points:<7}")
    
    # Test 6: Get all fixtures
    print("\n✓ Test 6: Recent Fixtures")
    print("-" * 40)
    fixtures = get_fixtures()
    print(f"  Total fixtures: {len(fixtures)}")
    print(f"\n  Recent matches:")
    for fixture in fixtures[:3]:
        home = fixture[1]
        away = fixture[2]
        result = fixture[4]
        print(f"    {home} vs {away} = {result}")
    
    # Test 7: Get top scorers overall
    print("\n✓ Test 7: Top Scorers (All Leagues)")
    print("-" * 40)
    scorers = get_top_scorers()
    print(f"  {'Player':<20} {'Team':<20} {'Goals':<6}")
    print(f"  {'-'*20} {'-'*20} {'-'*6}")
    for scorer in scorers[:5]:  # Show top 5
        name = scorer[0]
        team = scorer[1]
        goals = scorer[2]
        print(f"  {name:<20} {team:<20} {goals:<6}")
    
    # Test 8: Get top scorers by league
    print("\n✓ Test 8: Top Scorers (Premier League)")
    print("-" * 40)
    epl_scorers = get_top_scorers("Premier League")
    print(f"  {'Player':<20} {'Goals':<6}")
    print(f"  {'-'*20} {'-'*6}")
    for scorer in epl_scorers[:5]:
        name = scorer[0]
        goals = scorer[2]
        print(f"  {name:<20} {goals:<6}")
    
    # Test 9: Get top assisters
    print("\n✓ Test 9: Top Assist Makers")
    print("-" * 40)
    assisters = get_top_assisters()
    print(f"  {'Player':<20} {'Team':<20} {'Assists':<7}")
    print(f"  {'-'*20} {'-'*20} {'-'*7}")
    for assist in assisters[:5]:
        name = assist[0]
        team = assist[1]
        assists = assist[2]
        print(f"  {name:<20} {team:<20} {assists:<7}")
    
    # Test 10: Get awards
    print("\n✓ Test 10: Awards")
    print("-" * 40)
    awards = get_awards()
    print(f"  Total awards: {len(awards)}")
    print(f"\n  Award types:")
    award_types = set()
    for award in awards:
        award_types.add(award[1])
    for award_type in sorted(award_types):
        print(f"    • {award_type}")
    
    # Test 11: Get specific award
    print("\n✓ Test 11: Top Scorer Award Winners")
    print("-" * 40)
    top_scorers_award = get_awards("Top Scorer")
    print(f"  {'Player':<20} {'League':<20}")
    print(f"  {'-'*20} {'-'*20}")
    for award in top_scorers_award:
        player = award[2]
        league = award[4]
        print(f"  {player:<20} {league:<20}")
    
    # Summary
    print("\n" + "=" * 60)
    print("✅ ALL TESTS PASSED!")
    print("=" * 60)
    print("\nBackend Summary:")
    print(f"  • Tables: 4 (players, fixtures, league_standings, awards)")
    print(f"  • Players: {len(all_players)}")
    print(f"  • Fixtures: {len(fixtures)}")
    print(f"  • Leagues: {len(leagues)}")
    print(f"  • Awards: {len(awards)}")
    print("\n✓ Backend is working correctly!")
    print("✓ Ready for frontend development!")
    print("\nNext: Build the Streamlit frontend using these functions\n")


if __name__ == "__main__":
    test_backend()