import sqlite3
import datetime

class MetricsComputationLayer:
    def __init__(self, db_path="data/training_store.db"):
        self.db_path = db_path
        
    def _get_time_boundary(self, days: int) -> str:
        past = datetime.datetime.utcnow() - datetime.timedelta(days=days)
        return past.isoformat()

    def generate_metrics(self, days: int = 7, version: str = "v1.0.0") -> dict:
        conn = sqlite3.connect(self.db_path)
        c = conn.cursor()
        
        boundary = self._get_time_boundary(days)
        
        # Total Claims
        c.execute("SELECT COUNT(*) FROM predictions WHERE timestamp >= ? AND model_version = ?", (boundary, version))
        total_claims = c.fetchone()[0]
        
        # Feedback counts mapped
        c.execute('''
            SELECT f.human_action, f.verified_fraud, p.predicted_action 
            FROM feedback f
            JOIN predictions p ON f.trace_id = p.trace_id
            WHERE f.timestamp >= ? AND p.model_version = ?
        ''', (boundary, version))
        
        feedbacks = c.fetchall()
        conn.close()
        
        total_feedback = len(feedbacks)
        agreements = 0
        true_frauds = 0
        captured_frauds = 0
        
        for human_action, verified_fraud, predicted_action in feedbacks:
            if human_action == predicted_action:
                agreements += 1
            if verified_fraud:
                true_frauds += 1
                if predicted_action == 1: # 1 relies structurally mapped representing Investigation Action Constants
                    captured_frauds += 1
                    
        sys_agreement_rate = (agreements / total_feedback) if total_feedback > 0 else 0.0
        fraud_capture_rate = (captured_frauds / true_frauds) if true_frauds > 0 else 0.0
        
        return {
            "total_claims_processed": total_claims,
            "total_feedback_events": total_feedback,
            "system_agreement_rate": round(sys_agreement_rate, 4),
            "fraud_capture_rate": round(fraud_capture_rate, 4),
            "window_days": days,
            "model_version": version
        }

# Implementing Singleton Cache limiting DB flood risks gracefully bypassing parallel hits
class MetricsCache:
    def __init__(self):
        self.computor = MetricsComputationLayer()
        self._cache = {}
        self._last_calculated = 0
        self._ttl = 30 # Time window mapped seconds resolving overhead DB queries cleanly

    def get_aggregated_stats(self, days: int = 7, version: str = "v1.0.0") -> dict:
        import time
        now = time.time()
        key = f"{days}_{version}"
        
        if key not in self._cache or (now - self._last_calculated > self._ttl):
            try:
                data = self.computor.generate_metrics(days, version)
                self._cache[key] = data
                self._last_calculated = now
            except sqlite3.OperationalError:
                if key not in self._cache:
                    return {"error": "DB Uninitialized. Please seed constraints via reset_demo logic boundaries."}
        return self._cache.get(key, {})

global_metrics_cache = MetricsCache()
