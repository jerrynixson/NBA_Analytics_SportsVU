import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
import streamlit as st

def load_data():
    """
    Load NBA shot data with caching
    """
    return pd.read_csv('shots_fixed.csv')

def home_page(shots_df):
    """
    Render the home page of the dashboard
    """
    st.title("NBA Shot Analysis Dashboard")
    st.markdown("""
    ## Welcome to Advanced NBA Shot Analytics

    This dashboard provides in-depth insights into NBA shooting performance using advanced data analysis techniques.

    ### Key Analysis Areas:
    - **Shot Accuracy by Zone**: Understanding shooting effectiveness across different court areas
    - **Player Shooting Zones**: Identifying players' strengths in specific shooting locations
    - **Clutch Performance**: Analyzing player performance in critical game moments
    - **Shot type effectiveness**
    - **Shot position heatmaps**

    ### Data Insights Overview
    - **Total Shots Analyzed**: {total_shots}
    - **Unique Players**: {unique_players}
    - **Date Range**: {date_range}
    """.format(
        total_shots=len(shots_df),
        unique_players=shots_df['PLAYER_NAME'].nunique(),
        date_range=f"{shots_df['GAME_DATE'].min()} to {shots_df['GAME_DATE'].max()}"
    ))

def shot_accuracy_zone_page(shots_df):
    """
    Render shot accuracy by zone page
    """
    st.title("Shot Accuracy by Zone")
    
    # Compute zone accuracy
    zone_accuracy = shots_df.groupby('SHOT_ZONE_BASIC').agg({
        'SHOT_MADE_FLAG': ['mean', 'count']
    }).reset_index()
    zone_accuracy.columns = ['Shot Zone', 'Accuracy', 'Total Shots']
    zone_accuracy['Accuracy'] = zone_accuracy['Accuracy'] * 100

    # Visualization
    col1, col2 = st.columns([2, 1])
    
    with col1:
        fig, ax = plt.subplots(figsize=(10, 6))
        sns.barplot(
            x='Shot Zone', 
            y='Accuracy', 
            data=zone_accuracy, 
            palette='viridis'
        )
        plt.title('Shot Accuracy Across Different Zones')
        plt.xticks(rotation=45)
        plt.tight_layout()
        st.pyplot(fig)
    
    with col2:
        st.markdown("### Zone Accuracy Insights")
        st.dataframe(zone_accuracy)
        
        st.markdown("""
        #### Analysis Explanation
        - **Restricted Area**: Shots closest to the basket
        - **Mid-Range**: Shots from 8-16 feet
        - **3-Point Zone**: Shots beyond the 3-point line

        #### Key Observations
        - Compare shooting accuracy across different court zones
        - Identify most and least efficient shooting areas
        """)

def player_shooting_zones_page(shots_df):
    """
    Render player shooting zones page
    """
    st.title("Player Shooting Zones")
    
    # Player selection
    selected_player = st.selectbox(
        "Select Player", 
        sorted(shots_df['PLAYER_NAME'].unique())
    )
    
    # Filter data for selected player
    player_data = shots_df[shots_df['PLAYER_NAME'] == selected_player]
    
    # Compute player zone accuracy
    player_zone_accuracy = player_data.groupby('SHOT_ZONE_BASIC').agg({
        'SHOT_MADE_FLAG': ['mean', 'count']
    }).reset_index()
    player_zone_accuracy.columns = ['Shot Zone', 'Accuracy', 'Total Shots']
    player_zone_accuracy['Accuracy'] = player_zone_accuracy['Accuracy'] * 100

    # Visualization
    col1, col2 = st.columns([2, 1])
    
    with col1:
        fig, ax = plt.subplots(figsize=(10, 6))
        sns.barplot(
            x='Shot Zone', 
            y='Accuracy', 
            data=player_zone_accuracy, 
            palette='rocket'
        )
        plt.title(f'{selected_player} - Shooting Accuracy by Zone')
        plt.xticks(rotation=45)
        plt.tight_layout()
        st.pyplot(fig)
    
    with col2:
        st.markdown(f"### {selected_player} Zone Performance")
        st.dataframe(player_zone_accuracy)
        
        st.markdown("""
        #### Performance Insights
        - Analyze individual player's shooting strengths
        - Compare performance across different court zones
        - Identify optimal shooting areas for the player
        """)

def clutch_performance_page(shots_df):
    """
    Render clutch performance analysis page
    """
    st.title("Clutch Performance Analysis")
    
    # Define clutch time (last 2 minutes of 4th quarter)
    clutch_df = shots_df[
        (shots_df['PERIOD'] == 4) & 
        (shots_df['MINUTES_REMAINING'] <= 2)
    ]
    
    # Compute clutch performance
    clutch_analysis = clutch_df.groupby('PLAYER_NAME').agg({
        'SHOT_MADE_FLAG': ['mean', 'count']
    }).reset_index()
    clutch_analysis.columns = ['Player', 'Clutch Accuracy', 'Clutch Shots']
    clutch_analysis['Clutch Accuracy'] = clutch_analysis['Clutch Accuracy'] * 100
    
    # Filter for players with significant clutch attempts
    clutch_analysis = clutch_analysis[clutch_analysis['Clutch Shots'] >= 10]
    top_clutch_players = clutch_analysis.nlargest(10, 'Clutch Accuracy')

    # Visualization
    col1, col2 = st.columns([2, 1])
    
    with col1:
        fig, ax = plt.subplots(figsize=(10, 6))
        sns.barplot(
            x='Player', 
            y='Clutch Accuracy', 
            data=top_clutch_players, 
            palette='muted'
        )
        plt.title('Top 10 Players - Clutch Performance')
        plt.xticks(rotation=45)
        plt.tight_layout()
        st.pyplot(fig)
    
    with col2:
        st.markdown("### Clutch Performance Insights")
        st.dataframe(top_clutch_players)
        
        st.markdown("""
        #### Clutch Performance Definition
        - **Clutch Time**: Last 2 minutes of 4th quarter
        - **Minimum Attempts**: 10 shots
        
        #### Key Metrics
        - Shooting accuracy in high-pressure situations
        - Identifying players who perform best under pressure
        - Comparing clutch performance across players
        """)

def shot_type_effectiveness_page(shots_df):
    """
    Render shot type effectiveness page
    """
    st.title("Shot Type Effectiveness Analysis")
    
    # Compute shot type effectiveness
    shot_type_effectiveness = shots_df.groupby('SHOT_TYPE').agg({
        'SHOT_MADE_FLAG': ['mean', 'count']
    }).reset_index()
    shot_type_effectiveness.columns = ['Shot Type', 'Accuracy', 'Total Shots']
    shot_type_effectiveness['Accuracy'] = shot_type_effectiveness['Accuracy'] * 100
    shot_type_effectiveness['Percentage of Total Shots'] = (
        shot_type_effectiveness['Total Shots'] / len(shots_df) * 100
    )

    # Visualization columns
    col1, col2 = st.columns([2, 1])
    
    with col1:
        # Accuracy Bar Plot
        fig, ax = plt.subplots(figsize=(10, 6))
        sns.barplot(
            x='Shot Type', 
            y='Accuracy', 
            data=shot_type_effectiveness, 
            palette='coolwarm'
        )
        plt.title('Shot Accuracy by Shot Type')
        plt.ylabel('Accuracy (%)')
        plt.xticks(rotation=45)
        plt.tight_layout()
        st.pyplot(fig)

        # Pie Chart for Shot Distribution
        fig2, ax2 = plt.subplots(figsize=(8, 8))
        ax2.pie(
            shot_type_effectiveness['Total Shots'], 
            labels=shot_type_effectiveness['Shot Type'], 
            autopct='%1.1f%%',
            colors=sns.color_palette('pastel')
        )
        plt.title('Distribution of Shot Types')
        st.pyplot(fig2)
    
    with col2:
        st.markdown("### Shot Type Effectiveness Insights")
        
        # Display detailed table
        st.dataframe(shot_type_effectiveness)
        
        st.markdown("""
        #### Analysis Breakdown
        - **Accuracy**: Percentage of successful shots for each type
        - **Shot Distribution**: Proportion of total shots

        #### Key Observations
        - Compare effectiveness across different shot types
        - Understand shot selection strategies
        - Identify most efficient shooting techniques
        """)

def shot_location_heatmap_page(shots_df):
    """
    Render shot location heat maps page
    """
    st.title("Shot Location Heat Maps")
    
    # Player selection
    selected_player = st.selectbox(
        "Select Player for Heat Map", 
        sorted(shots_df['PLAYER_NAME'].unique())
    )
    
    # Filter data for selected player
    player_shots = shots_df[shots_df['PLAYER_NAME'] == selected_player]
    
    # Visualization columns
    col1, col2 = st.columns([2, 1])
    
    with col1:
        # Create heat map
        plt.figure(figsize=(12, 10))
        
        # Court background
        plt.xlim(-250, 250)
        plt.ylim(0, 470)
        
        # Add court lines (simplified)
        plt.axhline(y=0, color='black', linewidth=2)
        plt.axhline(y=470, color='black', linewidth=2)
        plt.axvline(x=-250, color='black', linewidth=2)
        plt.axvline(x=250, color='black', linewidth=2)
        
        # 3-point line (simplified)
        plt.plot([-220, 220], [0, 0], color='black', linewidth=2)
        
        # Heatmap of shot locations
        plt.title(f'{selected_player} - Shot Location Heat Map')
        plt.xlabel('Court X Coordinate')
        plt.ylabel('Court Y Coordinate')
        
        # Use seaborn kdeplot for heat map
        sns.kdeplot(
            x=player_shots['LOC_X'], 
            y=player_shots['LOC_Y'], 
            cmap='YlOrRd', 
            fill=True, 
            levels=10
        )
        
        plt.tight_layout()
        st.pyplot(plt)
    
    with col2:
        st.markdown(f"### {selected_player} Shot Location Analysis")
        
        # Shot distribution by accuracy
        shot_accuracy_by_zone = player_shots.groupby('SHOT_ZONE_BASIC')['SHOT_MADE_FLAG'].agg(['mean', 'count']).reset_index()
        shot_accuracy_by_zone.columns = ['Shot Zone', 'Accuracy', 'Total Shots']
        shot_accuracy_by_zone['Accuracy'] = shot_accuracy_by_zone['Accuracy'] * 100
        
        st.dataframe(shot_accuracy_by_zone)
        
        st.markdown("""
        #### Heat Map Interpretation
        - **Color Intensity**: Frequency of shots
        - **Brighter Areas**: More shots taken
        - **Darker Red**: Higher concentration of shots

        #### Key Insights
        - Visualize shooting preferences
        - Understand court positioning
        - Identify shooting hotspots
        """)

def main():
    # Page Configuration
    st.set_page_config(
        page_title="NBA Shot Analysis Dashboard", 
        page_icon=":basketball:", 
        layout="wide"
    )

    # Sidebar Navigation
    page = st.sidebar.selectbox(
        "Select Analysis Page", 
        [
            "Home", 
            "Shot Accuracy by Zone", 
            "Player Shooting Zones", 
            "Clutch Performance Analysis",
            "Shot Type Effectiveness",
            "Shot Location Heat Maps"
        ]
    )

    # Load data
    shots_df = load_data()

    # Page routing
    if page == "Home":
        home_page(shots_df)
    elif page == "Shot Accuracy by Zone":
        shot_accuracy_zone_page(shots_df)
    elif page == "Player Shooting Zones":
        player_shooting_zones_page(shots_df)
    elif page == "Clutch Performance Analysis":
        clutch_performance_page(shots_df)
    elif page == "Shot Type Effectiveness":
        shot_type_effectiveness_page(shots_df)
    elif page == "Shot Location Heat Maps":
        shot_location_heatmap_page(shots_df)

# Run the app
if __name__ == '__main__':
    main()