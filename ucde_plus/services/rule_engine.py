from models.schemas import FNOLRequest
from typing import Tuple, List

class RuleEngine:
    def __init__(self):
        self.high_amount_threshold = 10000.0
        self.suspicious_keywords = ["fraud", "suspicious", "staged", "intentional", "cash"]

    def evaluate(self, request: FNOLRequest) -> Tuple[float, float, List[str]]:
        fraud_score = 0.05
        severity_score = 0.10
        trace = []

        # Rule 1: High Claim Amount
        if request.claimAmount and request.claimAmount > self.high_amount_threshold:
            severity_score += 0.50
            fraud_score += 0.20
            trace.append(f"RULE_001_HIGH_AMOUNT: Claim exceeds threshold (${self.high_amount_threshold})")

        # Rule 2: Suspicious Keywords
        desc_lower = request.description.lower()
        if any(word in desc_lower for word in self.suspicious_keywords):
            fraud_score += 0.60
            trace.append("RULE_002_SUSPICIOUS_KEYWORD: Description contains flagged terminology.")

        # Ensure bounds
        fraud_score = min(1.0, fraud_score)
        severity_score = min(1.0, severity_score)

        return fraud_score, severity_score, trace
