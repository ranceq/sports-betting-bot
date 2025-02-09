import pandas as pd
import numpy as np
import os
from stable_baselines3 import PPO

def compute_confidence(predicted, implied):
    # Example formula: confidence is proportional to the positive difference
    # between predicted probability and implied probability.
    # Adjust the multiplier (e.g., 10) as needed to scale to 1-10.
    diff = predicted - implied
    confidence = diff * 10  # simple scaling factor
    # Clip confidence to be between 1 and 10 and round to 2 decimals.
    confidence = np.clip(confidence, 1, 10)
    return round(confidence, 2)

def generate_predictions():
    current_dir = os.path.dirname(os.path.abspath(__file__))
    odds_path = os.path.join(current_dir, "..", "data", "daily_odds.csv")
    df = pd.read_csv(odds_path)
    
    # Assume the odds field contains decimal odds.
    # Implied probability = 1 / odds.
    df['implied_prob'] = 1 / df['Odds'].astype(float)
    
    # For demonstration, simulate a predicted probability.
    # In a production system, you would use your RL model (and/or other models).
    np.random.seed(42)
    df['predicted_prob'] = df['implied_prob'] + np.random.uniform(-0.1, 0.1, size=len(df))
    df['predicted_prob'] = df['predicted_prob'].clip(0, 1)
    
    # Calculate confidence for each outcome.
    df['Confidence'] = df.apply(lambda row: compute_confidence(row['predicted_prob'], row['implied_prob']), axis=1)
    
    # Identify "good value" bets where predicted probability exceeds the implied probability.
    df['value'] = df['predicted_prob'] - df['implied_prob']
    
    # Save full daily results.
    output_path = os.path.join(current_dir, "..", "data", "daily_results.csv")
    df.to_csv(output_path, index=False)
    print("Daily results saved to", output_path)
    
    # Determine top 25 bets based on highest value (and optionally confidence).
    top25 = df.sort_values(by="value", ascending=False).head(25)
    top25_output = os.path.join(current_dir, "..", "data", "top25_bets.csv")
    top25.to_csv(top25_output, index=False)
    print("Top 25 bets saved to", top25_output)
    
    return top25

if __name__ == "__main__":
    generate_predictions()
