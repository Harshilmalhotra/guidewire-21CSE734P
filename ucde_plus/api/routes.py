from fastapi import APIRouter, Query, HTTPException, Request, Header
from models.schemas import FNOLRequest, FNOLResponse, FeedbackRequest
from services.orchestrator import AgenticOrchestrator
from services.db_client import SQLiteClient
from services.feedback_engine import global_feedback_engine
from services.logger import system_logger
from services.metrics import global_metrics_cache
import time

router = APIRouter(prefix="/v1")
orchestrator = AgenticOrchestrator()
db_client = SQLiteClient()

# Centralized in-memory mapping handling dummy API limits mitigating basic crawler scripts locally
RATE_LIMIT_STORE = {}

@router.post("/fnol", response_model=FNOLResponse, response_model_exclude_none=True)
async def submit_fnol(request: Request, payload: FNOLRequest, mode: str = Query("production")):
    client_ip = request.client.host if request.client else "unknown"
    now = time.time()
    
    if client_ip in RATE_LIMIT_STORE:
        req_count, start_window = RATE_LIMIT_STORE[client_ip]
        if now - start_window < 60:
            if req_count >= 10:
                raise HTTPException(status_code=429, detail="API rate limit exceeded. Please wait 60s")
            RATE_LIMIT_STORE[client_ip] = (req_count + 1, start_window)
        else:
            RATE_LIMIT_STORE[client_ip] = (1, now)
    else:
        RATE_LIMIT_STORE[client_ip] = (1, now)

    response = await orchestrator.process(payload)
    
    if mode != "debug":
        # Redaction by Design securely bounds the payload natively avoiding internal memory telemetry leakage
        response.decision_trace = None
        
    # JSON Structural Log bounds natively mapping exact latency traces cleanly capturing response logic
    latency_ms = (time.time() - now) * 1000
    system_logger.info(
        "Decision generated successfully natively caching limits explicitly",
        extra={"layer": "api", "trace_id": response.trace_id, "latency_ms": latency_ms, "status": "success"}
    )
    
    return response

@router.get("/metrics")
async def fetch_metrics(days: int = Query(7), model_version: str = Query("v1.0.0"), authorization: str = Header(None)):
    if authorization != "Bearer admin-api-token":
        system_logger.error("Unauthorized GET bounds execution natively aborted.", extra={"layer": "api", "status": "403"})
        raise HTTPException(status_code=403, detail="Unauthorized metrics view mapping.")
        
    stats = global_metrics_cache.get_aggregated_stats(days=days, version=model_version)
    if "error" in stats:
        raise HTTPException(status_code=500, detail=stats["error"])
        
    return stats

@router.post("/feedback")
async def submit_feedback(auth_payload: FeedbackRequest, authorization: str = Header(None)):
    if authorization != "Bearer adjuster-api-token":
        raise HTTPException(status_code=403, detail="Unauthorized Adjuster Feedback Scope.")
        
    trace = db_client.get_prediction(auth_payload.trace_id)
    if not trace:
        raise HTTPException(status_code=404, detail="Trace Logic Undefined")
        
    if trace["status"] == "finalized":
        raise HTTPException(status_code=409, detail="Trace feedback explicitly finalized. Avoiding Data poison loops natively.")
        
    # Translate math strictly parsing bounds
    human_action_int = 0 if auth_payload.human_action == "AUTO_APPROVE" else 1
    
    # Check consistency limits avoiding Garbage In
    if auth_payload.confidence == "LOW":
        raise HTTPException(status_code=422, detail="Explicit Uncertainty Filters Block low-confidence ground truth.")
        
    calculated_reward = global_feedback_engine.calculate_reward(human_action_int, auth_payload.verified_fraud)
    
    db_client.finalize_feedback(
        trace_id=auth_payload.trace_id,
        human_action=human_action_int,
        verified_fraud=auth_payload.verified_fraud,
        reward=calculated_reward,
        user_id="sys-adj-001",
        conf=auth_payload.confidence
    )
    
    return {"status": "Feedback committed explicitly into Batched Array Memory Constraints", "reward": calculated_reward}
