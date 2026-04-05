from pydantic import BaseModel
from typing import List, Optional, Dict, Any

class FNOLRequest(BaseModel):
    policyId: str
    policyholderId: str
    vehicleVin: Optional[str] = None
    description: str
    images: List[str]
    claimAmount: Optional[float] = None
    claimHistoryCount: int = 0
    timeSinceLastClaim: float = 0.0
    metadata: Optional[Dict[str, Any]] = None

class LLMInput(BaseModel):
    baseline_decision: str
    rl_decision: str
    fraud_score: float
    severity_score: float
    graph_risk_score: float
    expected_reward: float
    conflict_detected: bool

class LLMOutput(BaseModel):
    justification: str
    conflict_explanation: Optional[str] = None

class FNOLResponse(BaseModel):
    baselineDecision: str
    rlDecision: str
    expectedReward: float
    confidence: float
    graphRisk: float
    fraudScore: float
    decisionTrace: List[str]
    graphSignals: List[str] = []
    explanation: Optional[LLMOutput] = None
