import gymnasium as gym
from gymnasium import spaces
import numpy as np

class ClaimDecisionEnv(gym.Env):
    def __init__(self):
        super(ClaimDecisionEnv, self).__init__()
        # State: [severity_score, fraud_score, graph_risk, claim_amount_normalized]
        # Bounded between 0 and 1
        self.observation_space = spaces.Box(low=0.0, high=1.0, shape=(4,), dtype=np.float32)
        
        # Action: 0 = APPROVE, 1 = INVESTIGATE
        self.action_space = spaces.Discrete(2)
        
        # Current state
        self.state = None
        self.steps_taken = 0

    def reset(self, seed=None, options=None):
        super().reset(seed=seed)
        # Generate random state for synthetic training
        self.state = np.random.uniform(low=0.0, high=1.0, size=(4,)).astype(np.float32)
        self.steps_taken = 0
        return self.state, {}

    def step(self, action):
        severity, fraud, graph, amt = self.state
        
        # Ground-truth simulation rules (acts as the environment's implicit physics)
        should_investigate = (fraud > 0.5) or (graph > 0.4) or (severity > 0.8)
        
        reward = 0.0
        if action == 1: # INVESTIGATE
            if should_investigate:
                reward = 1.0  # Good catch! Minimal fraud loss
            else:
                reward = -0.5 # Wasted processing operational overhead
        else: # APPROVE
            if should_investigate:
                reward = -2.0 # Massive fraud payout loss (severe penalty)
            else:
                reward = 1.0  # Smooth, fast processing
                
        # Transition to next synthetic state
        self.state = np.random.uniform(low=0.0, high=1.0, size=(4,)).astype(np.float32)
        self.steps_taken += 1
        done = self.steps_taken >= 100
        
        return self.state, float(reward), done, False, {}
