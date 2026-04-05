from pydantic import BaseModel, ConfigDict, Field
from typing import Optional, Dict, Any, List

class FNOLRequest(BaseModel):
    policyId: str = Field(..., min_length=1)
    policyholderId: str = Field(..., min_length=1)
    vehicleVin: str = Field(..., min_length=1)
    description: str = Field(..., min_length=5)
    images: List[str]
    claimAmount: float = Field(..., gt=0)
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

class ScoresSchema(BaseModel):
    fraud: float
    severity: float
    graph: float
    fraud_breakdown: Optional[dict] = None
    graph_breakdown: Optional[dict] = None

class FNOLResponse(BaseModel):
    trace_id: str
    decision: str
    baseline_decision: str
    rl_decision: str
    scores: ScoresSchema
    expected_reward: float
    confidence_score: float
    explanation: Optional[LLMOutput] = None
    
    # Redaction parameters securely enforcing serialization
    decision_trace: Optional[List[str]] = None
    graph_signals: Optional[List[str]] = None

class FeedbackRequest(BaseModel):
    trace_id: str
    human_action: str # "AUTO_APPROVE" | "INVESTIGATE"
    verified_fraud: bool
    confidence: str # "HIGH" | "MEDIUM" | "LOW"
    comment: Optional[str] = None
