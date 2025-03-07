import os
import sys
from pathlib import Path
project_dir = Path(__file__).parent.parent

from yfpy.query import YahooFantasySportsQuery

def get_teams_data(query):
    """
    Get team data from Yahoo Fantasy Sports API and return as list of dictionaries.
    
    Args:
        query: YahooFantasySportsQuery object
        
    Returns:
        list: List of dictionaries containing team data with decoded strings
    """
    # Get teams from API
    league_teams = query.get_league_teams()
    
    # Create list to store team dictionaries
    teams = []
    
    # Get all attributes from first team to understand available fields
    team_attrs = [attr for attr in dir(league_teams[0]) if not attr.startswith('_')]
    
    # Create a dictionary for each team with all available attributes
    for team in league_teams:
        team_dict = {}
        for attr in team_attrs:
            try:
                # Get the attribute value if it exists
                value = getattr(team, attr)
                # Only include if it's not a method/function
                if not callable(value):
                    # Decode byte strings for name attribute
                    if attr == 'name' and isinstance(value, bytes):
                        team_dict[attr] = value.decode('utf-8')
                    else:
                        team_dict[attr] = value
            except AttributeError:
                # Skip if attribute doesn't exist
                continue
        teams.append(team_dict)
    
    return teams

def get_draft_results(query):
    """
    Get draft results from Yahoo Fantasy Sports API and return as list of dictionaries.
    
    Args:
        query: YahooFantasySportsQuery object
        
    Returns:
        list: List of dictionaries containing draft result data
    """
    # Get draft results from API
    draft_results = query.get_league_draft_results()
    
    # Create list to store draft result dictionaries
    results = []
    
    # Process each draft result
    for draft_result in draft_results:
        result_dict = {}
        
        # Get all attributes from draft result object
        draft_attrs = [attr for attr in dir(draft_result) if not attr.startswith('_')]
        
        # Extract each attribute
        for attr in draft_attrs:
            try:
                # Get the attribute value if it exists
                value = getattr(draft_result, attr)
                # Only include if it's not a method/function
                if not callable(value):
                    result_dict[attr] = value
            except AttributeError:
                # Skip if attribute doesn't exist
                continue
        
        # Add to results list
        results.append(result_dict)
    
    return results

if __name__ == "__main__":
    # Initialize query object
    query = YahooFantasySportsQuery(
        league_id="646316",
        game_code="nfl",
        game_id=449,  # NFL - 2024
        yahoo_consumer_key=os.environ.get("YAHOO_CONSUMER_KEY"),
        yahoo_consumer_secret=os.environ.get("YAHOO_CONSUMER_SECRET"),
        env_file_location=project_dir,
        save_token_data_to_env_file=True
    )
    
    # Get teams data
    teams = get_teams_data(query)
    draft_results = get_draft_results(query)
    
    # Print draft results information
    print("\n=== DRAFT RESULTS INSPECTION ===")
    print(f"Total draft picks: {len(draft_results)}")
    
    # Print available attributes for draft results
    print("\nAvailable draft result attributes:")
    if draft_results:
        print(sorted(draft_results[0].keys()))
    
    # Print first draft pick details
    print("\nFirst draft pick details:")
    if draft_results:
        first_pick = draft_results[0]
        for key, value in first_pick.items():
            print(f"{key}: {value}")
    
    # Print team information
    print("\n=== TEAM INFORMATION ===")
    print("Available team attributes:")
    print(sorted([attr for attr in teams[0].keys()]))
    print("\nTeam names:")
    for team in teams:
        print(f"Team name: {team['name']}")
    print("\nFirst team complete data:")
    for key, value in teams[0].items():
        print(f"{key}: {value}")



