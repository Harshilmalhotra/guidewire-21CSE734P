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
        
        # Total Claims and Baseline Disagreement Tracking
        c.execute("SELECT predicted_action, baseline_action, state_vector FROM predictions WHERE timestamp >= ? AND model_version = ?", (boundary, version))
        prediction_rows = c.fetchall()
        total_claims = len(prediction_rows)
        drift_count = sum([1 for r in prediction_rows if r[0] != r[1]])
        disagreement_rate = (drift_count / total_claims) if total_claims > 0 else 0.0
        
        # Macro Trigger Distribution securely tracking system behaviors
        import json
        trigger_dist = {"Severity": 0, "Fraud": 0, "Graph": 0}
        for r in prediction_rows:
            if r[0] == "INVESTIGATE":
                try:
                    s_vec = json.loads(r[2])
                    sev = s_vec[0]
                    frd = s_vec[1]
                    grph = s_vec[2]
                    if frd > 0.6: trigger_dist["Fraud"] += 1
                    elif grph > 0.7: trigger_dist["Graph"] += 1
                    elif sev > 0.5: trigger_dist["Severity"] += 1
                except:
                    pass
        total_trig = sum(trigger_dist.values())
        if total_trig > 0:
            for k in trigger_dist:
                trigger_dist[k] = round((trigger_dist[k] / total_trig) * 100, 1)
        
        # Explicit count of Ground Truth feedback events for 10/10 Enterprise training logic
        c.execute("SELECT COUNT(*) FROM feedback")
        total_feedback = c.fetchone()[0]
        
        # Feedback accuracy map
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
        
        # ML Evaluation Matrix cleanly bound naturally over Action Space (1=Investigate[Fraud], 0=Approve[Clean])
        # Mapping true_fraud as 1, predicted_fraud as 1
        tp, fp, fn, tn = 0, 0, 0, 0
        
        for human_action, verified_fraud, predicted_action in feedbacks:
            if human_action == predicted_action:
                agreements += 1
                
            # If ground truth was fraud (investigate)
            if verified_fraud:
                if predicted_action == 1:
                    tp += 1
                else:
                    fn += 1
            else: # ground truth was clean
                if predicted_action == 1:
                    fp += 1
                else:
                    tn += 1
                    
        sys_agreement_rate = (agreements / total_feedback) if total_feedback > 0 else 0.0
        
        precision = (tp / (tp + fp)) if (tp + fp) > 0 else 0.0
        recall = (tp / (tp + fn)) if (tp + fn) > 0 else 0.0
        f1 = (2 * precision * recall) / (precision + recall) if (precision + recall) > 0 else 0.0
        
        return {
            "total_claims_processed": total_claims,
            "total_feedback_events": len(feedbacks),
            "total_samples_collected": total_feedback,
            "system_agreement_rate": round(sys_agreement_rate, 4),
            "disagreement_drift_rate": round(disagreement_rate, 4),
            "trigger_distribution": trigger_dist,
            "precision": round(precision, 4),
            "recall": round(recall, 4),
            "f1_score": round(f1, 4),
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
