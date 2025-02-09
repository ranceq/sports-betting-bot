import gym
import numpy as np
from gym import spaces
from stable_baselines3 import PPO
import os

class BettingEnv(gym.Env):
    def __init__(self):
        super(BettingEnv, self).__init__()
        # Define three actions: bet on Home, bet on Away, or no bet.
        self.action_space = spaces.Discrete(3)
        # Define observation space with 4 dummy features (replace with real data features)
        self.observation_space = spaces.Box(low=0, high=1, shape=(4,), dtype=np.float32)
        self.state = np.random.rand(4)

    def step(self, action):
        # Dummy reward: if you bet, reward is a random value; if no bet, reward is 0.
        reward = 0 if action == 2 else np.random.uniform(-1, 1)
        self.state = np.random.rand(4)
        done = False  # Continuous environment; no terminal state.
        return self.state, reward, done, {}

    def reset(self):
        self.state = np.random.rand(4)
        return self.state

def train_rl_agent():
    env = BettingEnv()
    model = PPO("MlpPolicy", env, verbose=1)
    model.learn(total_timesteps=10000)
    
    current_dir = os.path.dirname(os.path.abspath(__file__))
    model_path = os.path.join(current_dir, "..", "models", "rl_betting_model")
    model.save(model_path)
    print("RL model trained and saved at", model_path)

if __name__ == "__main__":
    train_rl_agent()
