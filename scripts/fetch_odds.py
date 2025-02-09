import requests
import pandas as pd
import os
import json

def fetch_odds():
    # Dynamically determine the path to config.json
    current_dir = os.path.dirname(os.path.abspath(__file__))
    config_path = os.path.join(current_dir, "..", "config.json")
    
    # Load API key and other settings from config.json
    with open(config_path) as f:
        config = json.load(f)
    API_KEY = config["odds_api_key"]
    
    # Step 1: Retrieve the list of available sports
    sports_url = f"https://api.the-odds-api.com/v4/sports/?apiKey={API_KEY}"
    sports_response = requests.get(sports_url).json()
    
    # Extract the sport keys from the response
    sports = [sport['key'] for sport in sports_response]
    print("Retrieved sports:", sports)
    
    all_odds = []
    # Step 2: Loop through each sport and get odds
    for sport in sports:
        # Build the URL for the odds endpoint for this sport.
        # 'regions=us' specifies U.S. markets; 'markets=h2h' is head-to-head betting.
        odds_url = f"https://api.the-odds-api.com/v4/sports/{sport}/odds/?apiKey={API_KEY}&regions=us&markets=h2h,spreads,totals"
        response = requests.get(odds_url)
        
        if response.status_code != 200:
            print(f"Failed to retrieve odds for {sport}: {response.status_code}")
            continue
        
        games = response.json()
        for game in games:
            home_team = game.get("home_team", "Unknown")
            away_team = game.get("away_team", "Unknown")
            # Loop through each bookmaker providing odds for this game
            for bookmaker in game.get("bookmakers", []):
                bookmaker_title = bookmaker.get("title", "Unknown Bookmaker")
                # Each bookmaker may offer different markets
                for market in bookmaker.get("markets", []):
                    # Each market contains outcomes (e.g., Home win, Away win)
                    for outcome in market.get("outcomes", []):
                        odds_data = {
                            "Sport": sport,
                            "Match": f"{home_team} vs {away_team}",
                            "Outcome": outcome.get("name", ""),
                            "Odds": outcome.get("price", ""),
                            "Bookmaker": bookmaker_title,
                            "Market": market.get("key", "unknown")
                        }
                        all_odds.append(odds_data)
    
    # Save the collected odds data to a CSV file in the data folder.
    output_path = os.path.join(current_dir, "..", "data", "daily_odds.csv")
    df = pd.DataFrame(all_odds)
    df.to_csv(output_path, index=False)
    print("Daily odds saved successfully to", output_path)

if __name__ == "__main__":
    fetch_odds()
