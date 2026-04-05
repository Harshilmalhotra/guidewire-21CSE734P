import sqlite3
import os
import json
from datetime import datetime

DB_PATH = "data/training_store.db"

def reset_db():
    if os.path.exists(DB_PATH):
        os.remove(DB_PATH)
        
    os.makedirs(os.path.dirname(DB_PATH), exist_ok=True)
    conn = sqlite3.connect(DB_PATH)
    c = conn.cursor()
    c.execute('''
        CREATE TABLE IF NOT EXISTS predictions (
            trace_id TEXT PRIMARY KEY,
            state_vector TEXT NOT NULL,
            predicted_action INTEGER NOT NULL,
            model_version TEXT NOT NULL,
            timestamp DATETIME NOT NULL,
            status TEXT NOT NULL,
            baseline_action INTEGER DEFAULT 0
        )
    ''')
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
    
    # Insert Demo Seeds representing past states
    for i in range(50):
        t_id = f"seed-{i}"
        pred_act = i % 2
        base_act = 1 if (i % 4 == 0) else pred_act # introducing some simulated drift where baseline contradicts RL
        # Pred inserting
        c.execute('''
            INSERT INTO predictions (trace_id, state_vector, predicted_action, model_version, timestamp, status, baseline_action)
            VALUES (?, ?, ?, ?, ?, ?, ?)
        ''', (t_id, json.dumps([0.1, 0.05, 0, 0, 0, 0]), pred_act, "v1.0.0", datetime.utcnow().isoformat(), "finalized", base_act))

        
        # Determine pseudo-random agreement mapping parity mathematically capturing logical alignment simulations natively
        # Let's say 80% of the time, the adjuster agrees seamlessly natively
        human_act = pred_act if (i % 5 != 0) else (1 - pred_act)
        ver_fraud = True if human_act == 1 else False
        calculated_reward = 1.0 if human_act == pred_act else -1.0 # simplified stub log mapping natively
        
        c.execute('''
            INSERT INTO feedback (trace_id, human_action, verified_fraud, calculated_reward, adjuster_id, confidence, timestamp)
            VALUES (?, ?, ?, ?, ?, ?, ?)
        ''', (t_id, human_act, ver_fraud, calculated_reward, "sys-doc-00", "HIGH", datetime.utcnow().isoformat()))
        
    conn.commit()
    conn.close()
    print("Database reset and seeded with initial demo parameters natively.")

if __name__ == "__main__":
    reset_db()
