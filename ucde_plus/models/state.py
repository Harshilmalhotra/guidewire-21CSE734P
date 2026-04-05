from pydantic import BaseModel, ConfigDict
from typing import Optional, Dict, Any, List
from models.schemas import FNOLRequest

class ClaimContext(BaseModel):
    version: str = "v1"
    trace_id: str
    raw_input: FNOLRequest
    normalized_data: Dict[str, Any] = {}
    fraud_score: Optional[float] = None
    severity_score: Optional[float] = None
    graph_risk_score: Optional[float] = None
    fraud_breakdown: Optional[Dict[str, float]] = None
    graph_breakdown: Optional[Dict[str, float]] = None
    baseline_decision: Optional[str] = None
    rl_decision: Optional[str] = None
    expected_reward: Optional[float] = None
    confidence_score: Optional[float] = None
    decision_trace: List[str] = []
    graph_signals: List[str] = []

    model_config = ConfigDict(frozen=True) # Immutable contract

    def update(self, **kwargs) -> "ClaimContext":
        """Returns a new structured instance with updated fields reflecting safe immutability"""
        data = self.model_dump()
        # Clear out original lists to prevent duplicate append anomalies during dump unpacking
        current_trace = list(self.decision_trace)
        current_signals = list(self.graph_signals)
        
        for k, v in kwargs.items():
            if k == "decision_trace":
                current_trace.extend(v)
            elif k == "graph_signals":
                current_signals.extend(v)
            else:
                data[k] = v
                
        data["decision_trace"] = current_trace
        data["graph_signals"] = current_signals
        
        return ClaimContext(**data)
