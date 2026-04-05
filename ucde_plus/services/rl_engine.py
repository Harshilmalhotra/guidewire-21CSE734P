from stable_baselines3 import PPO
import numpy as np
import os

class RLEngine:
    def __init__(self):
        self.model_path = "ppo_claim_policy"
        if os.path.exists(self.model_path + ".zip"):
            self.model = PPO.load(self.model_path)
        else:
            raise Exception("RL model missing! You must pre-train by running: python train_rl.py")
            
    def predict(self, severity_score: float, fraud_score: float, graph_risk: float, claim_amount: float, history_count: int, time_since: float):
        norm_amt = min(1.0, (claim_amount or 0.0) / 20000.0)
        norm_hist = min(1.0, history_count / 10.0)
        norm_time = min(1.0, time_since / 365.0) 
        
        state = np.array([severity_score, fraud_score, graph_risk, norm_amt, norm_hist, norm_time], dtype=np.float32)
        
        # Use Epsilon-greedy internally implicitly baked via PPO ent_coef 
        action, _states = self.model.predict(state, deterministic=True)
        
        # Proxies V(s) evaluation from Critic head natively to determine expected business value
        import torch
        with torch.no_grad():
            obs = torch.tensor(state).unsqueeze(0)
            expected_reward = self.model.policy.predict_values(obs).item()
            
        rl_decision = "INVESTIGATE" if action == 1 else "AUTO_APPROVE"
        
        # Explicit RL logging simulating PROD pipeline engineering
        log_data = {
            "state": state.tolist(),
            "action": rl_decision,
            "reward": round(expected_reward, 2),
            "policy_confidence": "Evaluated Critically" # SB3 predict drops probs generically based on network distributions
        }
        print(f"\n[RL_ENGINE_LOG] {log_data}")
        
        return rl_decision, expected_reward
