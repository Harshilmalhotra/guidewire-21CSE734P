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
            status TEXT NOT NULL
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
        c.execute('''
            INSERT INTO predictions (trace_id, state_vector, predicted_action, model_version, timestamp, status)
            VALUES (?, ?, ?, ?, ?, ?)
        ''', (f"seed-{i}", json.dumps([0,0,0,0,0,0]), i % 2, "v1.0.0", datetime.utcnow().isoformat(), "pending"))
    
    conn.commit()
    conn.close()
    print("Database reset and seeded with initial demo parameters natively.")

if __name__ == "__main__":
    reset_db()
