import numpy as np
from stable_baselines3 import PPO
from services.rl_environment import ClaimDecisionEnv

def generate_structured_data(num_samples=25000):
    states = []
    labels = []
    for _ in range(num_samples):
        severity = np.random.uniform(0, 1)
        fraud = np.random.uniform(0, 1)
        graph = np.random.uniform(0, 1)
        amt = np.random.uniform(0, 1)
        hist = np.random.uniform(0, 1) # normalized count
        time_since = np.random.uniform(0, 1) # normalized days

        # Structured Correlation Logic for ground-truth synthesis:
        # If fraud_score > 0.7 AND graph_risk > 0.6, fraud is 95% likely
        if fraud > 0.7 and graph > 0.6:
            label = 1 if np.random.rand() > 0.05 else 0
        # If huge claim AND frequent history AND recent claim, fraud is 80% likely
        elif amt > 0.6 and hist > 0.7 and time_since < 0.2:
            label = 1 if np.random.rand() > 0.2 else 0
        # Clean safe claims
        elif fraud < 0.2 and graph < 0.2 and amt < 0.3:
            label = 0
        else:
            # Baseline background fraud rate: 10%
            label = 1 if np.random.rand() < 0.1 else 0
            
        states.append([severity, fraud, graph, amt, hist, time_since])
        labels.append(label)
        
    return np.array(states, dtype=np.float32), np.array(labels, dtype=np.int32)

if __name__ == "__main__":
    print("Generating Offline Structured Dataset...")
    states, labels = generate_structured_data(25000)
    
    # Init Env
    env = ClaimDecisionEnv()
    env.set_training_data(states, labels)
    
    print("Pre-training RL policy offline (Contextual Bandit PPO)....")
    # Epsilon-greedy exploration intrinsically via ent_coef entropy injection
    model = PPO("MlpPolicy", env, verbose=0, ent_coef=0.02)
    model.learn(total_timesteps=25000)
    
    model.save("ppo_claim_policy")
    print("RL policy successfully generated and saved to ppo_claim_policy.zip")
