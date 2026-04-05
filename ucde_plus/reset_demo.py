import sqlite3
import json
import os
import uuid
from datetime import datetime

def reset_db(db_path="data/training_store.db"):
    if os.path.exists(db_path):
        os.remove(db_path)
    
    os.makedirs(os.path.dirname(db_path), exist_ok=True)
    conn = sqlite3.connect(db_path)
    c = conn.cursor()
    
    # 1. Predictions Table
    c.execute('''
        CREATE TABLE IF NOT EXISTS predictions (
            trace_id TEXT PRIMARY KEY,
            state_vector TEXT NOT NULL,
            predicted_action INTEGER NOT NULL,
            baseline_action INTEGER NOT NULL,
            model_version TEXT NOT NULL,
            timestamp DATETIME NOT NULL,
            status TEXT NOT NULL
        )
    ''')
    
    # 2. Feedback Table
    c.execute('''
        CREATE TABLE IF NOT EXISTS feedback (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            trace_id TEXT NOT NULL,
            human_action INTEGER NOT NULL,
            verified_fraud BOOLEAN NOT NULL,
            calculated_reward REAL NOT NULL,
            adjuster_id TEXT NOT NULL,
            confidence TEXT NOT NULL,
            timestamp DATETIME NOT NULL,
            FOREIGN KEY(trace_id) REFERENCES predictions(trace_id)
        )
    ''')
    
    # Seed 12 diverse feedback samples (Triggering Training Readiness > 10)
    for i in range(12):
        trace_id = str(uuid.uuid4())
        is_fraud = (i % 3 == 0) # 4 Fraud, 8 Approved
        action_int = 1 if is_fraud else 0
        conf = "HIGH"
        reward = 1.0 if is_fraud else 0.5
        
        # State: [Severity, Fraud, Graph, Amount, History, Time]
        state = [0.6 if is_fraud else 0.1, 0.7 if is_fraud else 0.05, 0.5, 0.5, 0.5, 0.5]
        
        c.execute('''
            INSERT INTO predictions (trace_id, state_vector, predicted_action, baseline_action, model_version, timestamp, status)
            VALUES (?, ?, ?, ?, ?, ?, ?)
        ''', (trace_id, json.dumps(state), action_int, action_int, "v1.0.0", datetime.utcnow().isoformat(), "finalized"))
        
        c.execute('''
            INSERT INTO feedback (trace_id, human_action, verified_fraud, calculated_reward, adjuster_id, confidence, timestamp)
            VALUES (?, ?, ?, ?, ?, ?, ?)
        ''', (trace_id, action_int, is_fraud, reward, "sys-adj-001", conf, datetime.utcnow().isoformat()))
    
    conn.commit()
    conn.close()
    
    # Reset Registry
    registry_path = "data/model_registry.json"
    if os.path.exists(registry_path):
        os.remove(registry_path)
    
    print("Database and Registry reset and seeded with 12 feedback events natively.")

if __name__ == "__main__":
    reset_db()
