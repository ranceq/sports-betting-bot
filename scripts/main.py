import subprocess
import time
import os

def run_script(script_path):
    print(f"Running {script_path}...")
    result = subprocess.run(["python", script_path], capture_output=True, text=True)
    print(result.stdout)
    if result.returncode != 0:
        print(f"Error in {script_path}: {result.stderr}")
        exit(result.returncode)

def main_pipeline():
    # Step 1: Fetch today's betting odds using The Odds API.
    run_script("scripts/fetch_odds.py")
    
    # Step 2: Generate predictions and compute confidence values.
    run_script("scripts/predict_bets.py")
    
    # Step 3: Train (or fine-tune) the RL agent on previous day's results.
    run_script("scripts/enhanced_rl_model.py")

     # Step 4: Send top 25 bets to Discord.
    run_script("scripts/discord_bot.py")

    # Step 5: Export full daily results to Google Sheets.
    run_script("scripts/google_sheets.py")
    
    # (Optional) You can add more steps such as sending Discord notifications and exporting results to Google Sheets.
    print("Daily pipeline completed.")

if __name__ == "__main__":
    main_pipeline()
