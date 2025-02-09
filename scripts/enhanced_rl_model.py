import gym
import pandas as pd
import numpy as np
from gym import spaces
from stable_baselines3 import PPO
import os

class EnhancedHistoricalBettingEnv(gym.Env):
    """
    An RL environment that uses historical betting data to evaluate the agent’s predictions.
    The state consists of multiple features: Odds (normalized), RecentForm, and a healthy indicator (1 = healthy, 0 = injured).
    
    The agent outputs a continuous prediction (a float in [0,1]) representing its estimated win probability.
    
    Reward:
      - If the agent "bets" (i.e. its prediction >= bet_threshold), then:
         reward = normalized_confidence * ((Odds - 1) if Outcome == 1 else -1)
         where normalized_confidence = (prediction - bet_threshold) / (1 - bet_threshold).
      - If no bet is placed (prediction < bet_threshold), reward = 0.
    """
    def __init__(self, data_path, bet_threshold=0.5):
        super(EnhancedHistoricalBettingEnv, self).__init__()
        # Load historical data from CSV.
        self.data = pd.read_csv(data_path)
        self.bet_threshold = bet_threshold
        self.current_index = 0
        # Assume data contains: "Odds", "RecentForm", "InjuryStatus", "Outcome"
        # We'll represent the state as a vector: [normalized Odds, RecentForm, HealthyIndicator]
        # Normalized Odds: odds divided by 100 (assumes odds roughly in [1, 100])
        # HealthyIndicator: 1 if InjuryStatus is 0, else 0.
        self.observation_space = spaces.Box(low=0.0, high=1.0, shape=(3,), dtype=np.float32)
        # Action: a continuous value between 0 and 1 (the predicted probability)
        self.action_space = spaces.Box(low=0.0, high=1.0, shape=(1,), dtype=np.float32)

    def step(self, action):
        if self.current_index >= len(self.data):
            return np.array([0.0, 0.0, 0.0], dtype=np.float32), 0.0, True, {}
        
        # Get current match data.
        row = self.data.iloc[self.current_index]
        odds = float(row["Odds"])           # e.g., 1.5, 2.0, etc.
        recent_form = float(row["RecentForm"])  # normalized between 0 and 1
        injury_status = float(row["InjuryStatus"])  # 0 or 1 (0 means healthy)
        healthy_indicator = 1.0 - injury_status  # 1 if healthy, 0 if injured

        # State: normalized odds (divide by 100 for example), recent form, healthy indicator.
        state = np.array([odds / 100.0, recent_form, healthy_indicator], dtype=np.float32)
        actual_outcome = int(row["Outcome"])  # 1 for win, 0 for loss

        # The agent's action is its predicted win probability.
        prediction = float(action[0])
        
        # Calculate reward:
        if prediction >= self.bet_threshold:
            normalized_confidence = (prediction - self.bet_threshold) / (1 - self.bet_threshold)
            # Reward: scaled by potential profit (odds - 1) if win, negative reward if loss.
            reward = normalized_confidence * ((odds - 1) if actual_outcome == 1 else -1)
        else:
            reward = 0.0

        self.current_index += 1
        done = self.current_index >= len(self.data)
        return state, reward, done, {}

    def reset(self):
        self.current_index = 0
        row = self.data.iloc[0]
        odds = float(row["Odds"])
        recent_form = float(row["RecentForm"])
        injury_status = float(row["InjuryStatus"])
        healthy_indicator = 1.0 - injury_status
        state = np.array([odds / 100.0, recent_form, healthy_indicator], dtype=np.float32)
        return state

def train_enhanced_rl_agent():
    current_dir = os.path.dirname(os.path.abspath(__file__))
    data_path = os.path.join(current_dir, "..", "data", "previous_day_results.csv")
    env = EnhancedHistoricalBettingEnv(data_path, bet_threshold=0.5)
    
    model = PPO("MlpPolicy", env, verbose=1)
    model.learn(total_timesteps=10000)
    
    model_path = os.path.join(current_dir, "..", "models", "enhanced_rl_model")
    model.save(model_path)
    print("Enhanced RL model trained and saved at", model_path)

if __name__ == "__main__":
    train_enhanced_rl_agent()
