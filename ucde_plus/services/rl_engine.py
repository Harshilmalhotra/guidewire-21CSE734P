from stable_baselines3 import PPO
from services.rl_environment import ClaimDecisionEnv
import numpy as np
import os

class RLEngine:
    def __init__(self):
        self.env = ClaimDecisionEnv()
        self.model_path = "ppo_claim_policy"
        if os.path.exists(self.model_path + ".zip"):
            self.model = PPO.load(self.model_path)
            print("Loaded trained RL policy.")
        else:
            print("Training initial RL policy...")
            self.model = PPO("MlpPolicy", self.env, verbose=0)
            self.model.learn(total_timesteps=5000)
            self.model.save(self.model_path)
            
    def predict(self, severity_score: float, fraud_score: float, graph_risk: float, claim_amount: float):
        # Normalize the raw claim amount logically (assuming 20k is max standard bound for scaling)
        norm_amt = min(1.0, (claim_amount or 0.0) / 20000.0)
        
        state = np.array([severity_score, fraud_score, graph_risk, norm_amt], dtype=np.float32)
        action, _states = self.model.predict(state, deterministic=True)
        
        decision = "INVESTIGATE" if action == 1 else "APPROVE"
        return decision
