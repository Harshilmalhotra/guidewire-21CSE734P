from pydantic import BaseModel
from typing import List, Optional, Dict, Any

class FNOLRequest(BaseModel):
    policyId: str
    policyholderId: str
    vehicleVin: Optional[str] = None
    description: str
    images: List[str]
    claimAmount: Optional[float] = None
    metadata: Optional[Dict[str, Any]] = None

class FNOLResponse(BaseModel):
    decision: str
    confidence: float
    graphRisk: float
    fraudScore: float
    decisionTrace: List[str]
