import sqlite3
import json
import os
from datetime import datetime

class SQLiteClient:
    def __init__(self, db_path="data/training_store.db"):
        os.makedirs(os.path.dirname(db_path), exist_ok=True)
        self.db_path = db_path
        self._init_db()

    def _init_db(self):
        conn = sqlite3.connect(self.db_path)
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
        conn.commit()
        conn.close()

    def insert_prediction(self, trace_id: str, state_vector: list, action_str: str, version: str, baseline_action_str: str = "AUTO_APPROVE"):
        conn = sqlite3.connect(self.db_path)
        c = conn.cursor()
        try:
            act_int = 1 if action_str == "INVESTIGATE" else 0
            base_int = 1 if baseline_action_str == "INVESTIGATE" else 0
            
            c.execute('''
                INSERT INTO predictions (trace_id, state_vector, predicted_action, model_version, timestamp, status, baseline_action)
                VALUES (?, ?, ?, ?, ?, ?, ?)
            ''', (trace_id, json.dumps(state_vector), act_int, version, datetime.utcnow().isoformat(), "pending", base_int))
            conn.commit()
        except sqlite3.IntegrityError:
            pass # Idempotent log mapping
        finally:
            conn.close()

    def get_prediction(self, trace_id: str):
        conn = sqlite3.connect(self.db_path)
        c = conn.cursor()
        c.execute("SELECT state_vector, predicted_action, status FROM predictions WHERE trace_id = ?", (trace_id,))
        res = c.fetchone()
        conn.close()
        if res:
            return {
                "state_vector": json.loads(res[0]),
                "predicted_action": res[1],
                "status": res[2]
            }
        return None

    def finalize_feedback(self, trace_id: str, human_action: int, verified_fraud: bool, reward: float, user_id: str, conf: str):
        conn = sqlite3.connect(self.db_path)
        c = conn.cursor()
        try:
            c.execute(
                "INSERT INTO feedback (trace_id, human_action, verified_fraud, calculated_reward, adjuster_id, confidence, timestamp) VALUES (?, ?, ?, ?, ?, ?, ?)",
                (trace_id, human_action, verified_fraud, reward, user_id, conf, datetime.utcnow().isoformat())
            )
            c.execute("UPDATE predictions SET status = 'finalized' WHERE trace_id = ?", (trace_id,))
            conn.commit()
        except Exception:
            conn.rollback()
            raise
        finally:
            conn.close()
