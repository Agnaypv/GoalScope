import streamlit as st
import pandas as pd
from db import (
    search_player, 
    get_league_table, 
    get_top_scorers, 
    get_top_assisters,
    get_all_leagues,
    get_awards
)

# Set page config
st.set_page_config(
    page_title="Football Stats Explorer",
    page_icon="⚽",
    layout="wide"
)

# Title
st.title("⚽ Football Stats Explorer")
st.write("Search players, browse league tables, and explore awards from top European leagues")

# Sidebar for navigation
page = st.sidebar.radio(
    "Select Page:",
    ["🔍 Player Search", "📊 League Tables", "🏆 Awards & Top Scorers"]
)

# PAGE 1: PLAYER SEARCH
if page == "🔍 Player Search":
    st.header("Search Players")
    
    # Search input
    search_name = st.text_input("Enter player name:", placeholder="e.g., Haaland, Salah, Benzema")
    
    if search_name:
        # Search in database
        results = search_player(search_name)
        
        if results:
            st.success(f"Found {len(results)} player(s)")
            
            # Display each result
            for player in results:
                with st.container():
                    col1, col2 = st.columns(2)
                    
                    with col1:
                        st.subheader(player[1])  # Player name
                        st.write(f"**Team:** {player[2]}")
                        st.write(f"**Position:** {player[3]}")
                        st.write(f"**Nationality:** {player[7]}")
                        st.write(f"**Age:** {player[8]}")
                    
                    with col2:
                        st.write(f"**League:** {player[10]}")
                        st.write(f"**Goals:** {player[4]}")
                        st.write(f"**Assists:** {player[5]}")
                        st.write(f"**Appearances:** {player[6]}")
                        st.write(f"**Rating:** {player[9]}")
                    
                    st.divider()
        else:
            st.warning("No players found. Try searching for: Haaland, Salah, Benzema, Mbappé, etc.")


# PAGE 2: LEAGUE TABLES
elif page == "📊 League Tables":
    st.header("League Standings")
    
    # Get all leagues
    leagues = get_all_leagues()
    
    # Select league
    selected_league = st.selectbox("Select a league:", leagues)
    
    if selected_league:
        # Get standings
        standings = get_league_table(selected_league)
        
        if standings and len(standings) > 0:
            # Create list of dictionaries for DataFrame
            data_list = []
            for standing in standings:
                # standing is a tuple: (id, league, position, team, played, wins, draws, losses, gf, ga, points)
                data_list.append({
                    'Position': standing[2],
                    'Team': standing[3],
                    'Played': standing[4],
                    'Wins': standing[5],
                    'Draws': standing[6],
                    'Losses': standing[7],
                    'Points': standing[10]
                })
            
            df = pd.DataFrame(data_list)
            
            st.write(f"### {selected_league}")
            st.dataframe(df, use_container_width=True, hide_index=True)
            
            # Summary stats
            if len(df) > 0:
                col1, col2, col3 = st.columns(3)
                col1.metric("Top Team", df.iloc[0]['Team'], int(df.iloc[0]['Points']))
                col2.metric("Matches Played", int(df.iloc[0]['Played']))
                col3.metric("Total Teams", len(df))
        else:
            st.warning("No standings found for this league.")


# PAGE 3: AWARDS & TOP SCORERS
elif page == "🏆 Awards & Top Scorers":
    st.header("Awards, Top Scorers & Assist Makers")
    
    # Get leagues for filtering
    leagues = get_all_leagues()
    selected_league = st.selectbox("Select league (or view all):", ["All"] + leagues)
    
    # TOP SCORERS
    st.subheader("🔥 Top Scorers")
    
    if selected_league == "All":
        top_scorers = get_top_scorers()
    else:
        top_scorers = get_top_scorers(selected_league)
    
    if top_scorers and len(top_scorers) > 0:
        scorers_list = []
        for rank, scorer in enumerate(top_scorers, 1):
            scorers_list.append({
                'Rank': rank,
                'Player': scorer[0],
                'Team': scorer[1],
                'Goals': scorer[2]
            })
        scorers_df = pd.DataFrame(scorers_list)
        st.dataframe(scorers_df, use_container_width=True, hide_index=True)
    else:
        st.info("No scorers found.")
    
    st.divider()
    
    # TOP ASSIST MAKERS
    st.subheader("⚡ Top Assist Makers")
    
    if selected_league == "All":
        top_assisters = get_top_assisters()
    else:
        top_assisters = get_top_assisters(selected_league)
    
    if top_assisters and len(top_assisters) > 0:
        assisters_list = []
        for rank, assister in enumerate(top_assisters, 1):
            assisters_list.append({
                'Rank': rank,
                'Player': assister[0],
                'Team': assister[1],
                'Assists': assister[2]
            })
        assisters_df = pd.DataFrame(assisters_list)
        st.dataframe(assisters_df, use_container_width=True, hide_index=True)
    else:
        st.info("No assist makers found.")
    
    st.divider()
    
    # AWARDS
    st.subheader("🏅 Awards & Achievements")
    
    awards = get_awards()
    
    if awards and len(awards) > 0:
        awards_list = []
        for award in awards:
            awards_list.append({
                'Award': award[1],
                'Player': award[2],
                'League': award[4]
            })
        awards_df = pd.DataFrame(awards_list)
        st.dataframe(awards_df, use_container_width=True, hide_index=True)
    else:
        st.info("No awards found.")

# Footer
st.divider()
st.write("*Data from Football Stats Explorer • Updated: 2024*")