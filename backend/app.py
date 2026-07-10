"""
Football Stats Explorer - Streamlit Frontend
Built with Python + Streamlit
"""

import streamlit as st
from db import (
    search_player,
    get_all_leagues,
    get_league_table,
    get_fixtures,
    get_top_scorers,
    get_top_assisters,
    get_awards
)

# Page config
st.set_page_config(
    page_title="Football Stats Explorer",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Custom styling
st.markdown("""
    <style>
    .title-text {
        font-size: 2.5rem;
        font-weight: bold;
        color: #1f77b4;
    }
    </style>
""", unsafe_allow_html=True)

# ==================== APP HEADER ====================
st.title("⚽ Football Stats Explorer")
st.markdown("Explore player stats, league tables, and fixtures from 5 major European leagues")

# Sidebar navigation
page = st.sidebar.selectbox(
    "📍 Choose Page:",
    ["Home", "Player Search", "League Tables", "Fixtures", "Awards"]
)

# ==================== HOME PAGE ====================
if page == "Home":
    col1, col2 = st.columns([2, 1])
    
    with col1:
        st.header("Welcome to Football Stats Explorer")
        
        st.write("""
        This app gives you instant access to football statistics from the top 5 European leagues:
        
        🏴󠁧󠁢󠁥󠁮󠁧󠁿 **Premier League** (England)
        🇪🇸 **La Liga** (Spain)
        🇮🇹 **Serie A** (Italy)
        🇩🇪 **Bundesliga** (Germany)
        🇫🇷 **Ligue 1** (France)
        
        ### Features:
        - 🔍 **Player Search** - Find any player and see their complete statistics
        - 📊 **League Tables** - Current standings for all 5 leagues
        - ⚽ **Fixtures** - Upcoming matches and recent results
        - 🏆 **Awards** - Top scorers, assist makers, and achievements
        
        ### How to use:
        1. Select a page from the menu on the left
        2. Enter search criteria or select from dropdowns
        3. Click the button to view results
        4. Explore the data!
        """)
    
    with col2:
        st.metric("Leagues", "5")
        st.metric("Players", "50+")
        st.metric("Matches", "50+")
        st.metric("Awards", "20+")

# ==================== PLAYER SEARCH PAGE ====================
elif page == "Player Search":
    st.header("🔍 Player Search")
    st.write("Search for any player and view their detailed statistics")
    
    # Search input
    col1, col2 = st.columns([3, 1])
    
    with col1:
        player_name = st.text_input(
            "Enter player name:",
            placeholder="e.g., Haaland, Salah, Benzema",
            key="player_search"
        )
    
    with col2:
        search_button = st.button("🔎 Search", use_container_width=True, key="search_btn")
    
    if search_button:
        if player_name.strip():
            results = search_player(player_name)
            
            if results:
                st.success(f"✅ Found {len(results)} player(s) matching '{player_name}'")
                st.divider()
                
                for idx, player in enumerate(results):
                    # Player info
                    col1, col2, col3 = st.columns(3)
                    
                    with col1:
                        st.subheader(player[1])
                        st.write(f"**Team:** {player[2]}")
                        st.write(f"**League:** {player[10]}")
                    
                    with col2:
                        st.write(f"**Position:** {player[3]}")
                        st.write(f"**Age:** {player[8]}")
                        st.write(f"**Nationality:** {player[7]}")
                    
                    with col3:
                        st.write(f"**Goals:** {player[4]}")
                        st.write(f"**Assists:** {player[5]}")
                        st.write(f"**Appearances:** {player[6]}")
                        st.write(f"**Rating:** {player[9]}")
                    
                    if idx < len(results) - 1:
                        st.divider()
            else:
                st.warning(f"❌ No players found matching '{player_name}'. Try another name.")
        else:
            st.info("ℹ️ Please enter a player name to search")

# ==================== LEAGUE TABLES PAGE ====================
elif page == "League Tables":
    st.header("📊 League Standings")
    st.write("Current standings for all 5 major European leagues")
    st.divider()
    
    # Get all leagues
    leagues = get_all_leagues()
    
    # League selector
    col1, col2 = st.columns([3, 1])
    
    with col1:
        selected_league = st.selectbox(
            "Select League:",
            leagues,
            key="league_select"
        )
    
    with col2:
        show_button = st.button("📋 Show Table", use_container_width=True, key="show_table_btn")
    
    if show_button:
        standings = get_league_table(selected_league)
        
        if standings:
            st.success(f"✅ {selected_league} Standings")
            st.divider()
            
            # Format data for table
            table_data = []
            for row in standings:
                table_data.append({
                    "Pos": row[3],
                    "Team": row[4],
                    "P": row[5],
                    "W": row[6],
                    "D": row[7],
                    "L": row[8],
                    "GF": row[9],
                    "GA": row[10],
                    "GD": row[9] - row[10],
                    "Pts": row[11]
                })
            
            st.table(table_data)
            
            st.caption("P=Played, W=Wins, D=Draws, L=Losses, GF=Goals For, GA=Goals Against, GD=Goal Difference, Pts=Points")
        else:
            st.warning("❌ No data found for this league")

# ==================== FIXTURES PAGE ====================
elif page == "Fixtures":
    st.header("⚽ Matches & Fixtures")
    st.write("Upcoming and recent matches from all leagues")
    st.divider()
    
    if st.button("📅 Show All Matches", use_container_width=True, key="show_fixtures_btn"):
        fixtures = get_fixtures()
        
        if fixtures:
            st.success(f"✅ Found {len(fixtures)} matches")
            st.divider()
            
            for idx, fixture in enumerate(fixtures):
                # Match details
                col1, col2, col3 = st.columns([2, 1, 2])
                
                with col1:
                    st.write(f"**🏠 {fixture[1]}**")
                
                with col2:
                    st.write("**vs**")
                
                with col3:
                    st.write(f"**🏃 {fixture[2]}**")
                
                # Match info
                col1, col2, col3, col4 = st.columns(4)
                
                with col1:
                    st.caption(f"📅 {fixture[3]}")
                
                with col2:
                    st.caption(f"🎯 {fixture[4]}")
                
                with col3:
                    st.caption(f"⚽ {fixture[5]}")
                
                with col4:
                    pass
                
                if idx < len(fixtures) - 1:
                    st.divider()
        else:
            st.warning("❌ No fixtures found")

# ==================== AWARDS PAGE ====================
elif page == "Awards":
    st.header("🏆 Awards & Achievements")
    st.write("Top scorers, assist makers, and special awards")
    st.divider()
    
    # Award type selector
    award_type = st.selectbox(
        "Select Award Type:",
        ["Top Scorers", "Top Assisters", "All Awards"],
        key="award_select"
    )
    
    if st.button("🏆 Show Awards", use_container_width=True, key="show_awards_btn"):
        
        if award_type == "Top Scorers":
            st.subheader("⚽ Top Goal Scorers (All Leagues)")
            st.divider()
            
            scorers = get_top_scorers()
            
            table_data = []
            for i, scorer in enumerate(scorers, 1):
                table_data.append({
                    "Rank": i,
                    "Player": scorer[0],
                    "Team": scorer[1],
                    "Goals": scorer[2],
                    "League": scorer[3]
                })
            
            st.table(table_data)
        
        elif award_type == "Top Assisters":
            st.subheader("🎯 Top Assist Makers (All Leagues)")
            st.divider()
            
            assisters = get_top_assisters()
            
            table_data = []
            for i, assister in enumerate(assisters, 1):
                table_data.append({
                    "Rank": i,
                    "Player": assister[0],
                    "Team": assister[1],
                    "Assists": assister[2],
                    "League": assister[3]
                })
            
            st.table(table_data)
        
        else:  # All Awards
            st.subheader("🌟 All Awards & Achievements")
            st.divider()
            
            all_awards = get_awards()
            
            table_data = []
            for award in all_awards:
                table_data.append({
                    "Award": award[1],
                    "Player": award[2],
                    "Season": award[3],
                    "League": award[4]
                })
            
            st.table(table_data)

# ==================== FOOTER ====================
st.divider()
col1, col2, col3 = st.columns(3)

with col1:
    st.caption("✅ Football Stats Explorer")

with col2:
    st.caption("Built with Python + Streamlit")

with col3:
    st.caption("© 2024 Bootcamp Project")