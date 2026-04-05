import gymnasium as gym
from gymnasium import spaces
import numpy as np

class ClaimDecisionEnv(gym.Env):
    def __init__(self):
        super(ClaimDecisionEnv, self).__init__()
        # State [6-dim]: Contextual vectors including historical attributes
        self.observation_space = spaces.Box(low=0.0, high=1.0, shape=(6,), dtype=np.float32)
        
        # Action: 0 = AUTO_APPROVE, 1 = INVESTIGATE
        self.action_space = spaces.Discrete(2)
        
        self.states = None
        self.labels = None
        self.current_idx = 0
        self.max_idx = 0
        
        self.state = np.zeros(6, dtype=np.float32)
        
    def set_training_data(self, states, labels):
        self.states = states
        self.labels = labels
        self.max_idx = len(states)
        self.current_idx = 0

    def reset(self, seed=None, options=None):
        super().reset(seed=seed)
        if self.states is not None and self.current_idx < self.max_idx:
            self.state = self.states[self.current_idx]
        else:
            self.state = np.random.uniform(low=0.0, high=1.0, size=(6,)).astype(np.float32)
        return self.state, {}

    def step(self, action):
        # We model this as a contextual bandit problem (single-step RL), not full sequential MDP, to keep scope tractable.
        
        if self.labels is not None and self.current_idx < self.max_idx:
            true_fraud_label = self.labels[self.current_idx]
        else:
            true_fraud_label = 0
            
        reward = 0.0
        processing_time_penalty = 1.0 # Base operational drag
        
        # Explicit Business Reward Mapping
        if action == 0:  # AUTO_APPROVE
            if true_fraud_label == 1:
                reward -= 100.0   # Fraud loss (HIGH penalty)
            else:
                reward += 10.0    # Fast processing benefit
        elif action == 1: # INVESTIGATE
            if true_fraud_label == 1:
                reward += 50.0    # Prevented massive fraud payout
            else:
                reward -= 10.0    # Unnecessary adjuster operational friction cost
                
        # Universal friction penalty
        reward -= processing_time_penalty
        
        self.current_idx += 1
        
        # Bandits conclude per-step uniformly via `done=True`
        done = True 
        
        return self.state, float(reward), done, False, {}
