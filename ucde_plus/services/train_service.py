import sqlite3
import json
import os
import numpy as np
from datetime import datetime
from stable_baselines3 import PPO
from services.rl_environment import ClaimDecisionEnv
from services.model_registry import global_model_registry

class RLTrainingService:
    def __init__(self, db_path="data/training_store.db"):
        self.db_path = db_path
        self.status = "IDLE" # IDLE, RUNNING, COMPLETED, FAILED
        self.last_run_stats = {}

    def fetch_feedback_data(self):
        """Pulls ground truth feedback from training_store.db."""
        conn = sqlite3.connect(self.db_path)
        c = conn.cursor()
        c.execute('''
            SELECT p.state_vector, f.human_action 
            FROM predictions p
            JOIN feedback f ON p.trace_id = f.trace_id
            WHERE p.status = 'finalized'
        ''')
        rows = c.fetchall()
        conn.close()
        
        if len(rows) < 10: # DEMO LIMIT: Allow local training if n < 50 for testing, but ideally 50+
            return [], []
            
        states = [json.loads(r[0]) for r in rows]
        labels = [r[1] for r in rows]
        return np.array(states, dtype=np.float32), np.array(labels, dtype=np.int32)

    def train(self):
        self.status = "RUNNING"
        try:
            states, labels = self.fetch_feedback_data()
            
            # Implementation of 80/20 Train/Validation Split
            num_samples = len(states)
            if num_samples < 10:
                 self.status = "FAILED"
                 self.last_run_stats = {"error": "Insufficient samples (n < 10)"}
                 return
            
            indices = np.arange(num_samples)
            np.random.shuffle(indices)
            split_idx = int(num_samples * 0.8)
            
            train_idx, val_idx = indices[:split_idx], indices[split_idx:]
            
            # Init Env
            env = ClaimDecisionEnv()
            env.set_training_data(states[train_idx], labels[train_idx])
            
            # Pre-training Offline RL
            model = PPO("MlpPolicy", env, verbose=0, ent_coef=0.02)
            model.learn(total_timesteps=max(5000, num_samples * 10))
            
            # Validation Step
            correct = 0
            for idx in val_idx:
                s = states[idx]
                true_label = labels[idx]
                action, _ = model.predict(s, deterministic=True)
                if action == true_label:
                    correct += 1
            
            val_acc = (correct / len(val_idx)) if len(val_idx) > 0 else 0.0
            
            # Versioning & Registration
            new_v_name = f"data/models/ppo_v{datetime.now().strftime('%M%S')}.zip"
            model.save(new_v_name)
            
            active_v = global_model_registry.register_new_version(
                path=new_v_name, 
                accuracy=val_acc, 
                samples=num_samples
            )
            
            self.status = "COMPLETED"
            self.last_run_stats = {
                "active_version": active_v,
                "val_accuracy": val_acc,
                "samples": num_samples,
                "timestamp": datetime.now().isoformat()
            }
            
        except Exception as e:
            self.status = "FAILED"
            self.last_run_stats = {"error": str(e)}

global_training_service = RLTrainingService()
