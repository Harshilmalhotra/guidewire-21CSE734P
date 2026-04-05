import asyncio
import time
import json
import hashlib
from typing import Tuple
from models.state import ClaimContext
from services.rule_engine import RuleEngine
from services.graph_intelligence import GraphIntelligenceEngine
from services.graph_builder import global_graph_service

def emit_log(agent_name: str, input_hash: str, output_fields: dict, latency_ms: float, status: str):
    log_entry = {
        "agent_name": agent_name,
        "input_hash": input_hash,
        "output_fields": output_fields,
        "latency_ms": round(latency_ms, 2),
        "status": status
    }
    print(f"[AGENT_TRACE] {json.dumps(log_entry)}")

class IntakeAgent:
    def execute(self, request) -> ClaimContext:
        start_time = time.time()
        import uuid
        trace_id = str(uuid.uuid4())
        
        input_hash = hashlib.md5(request.model_dump_json().encode()).hexdigest()
        
        ctx = ClaimContext(
            trace_id=trace_id,
            raw_input=request,
            normalized_data={"processed_at": start_time}
        )
        
        emit_log(
            agent_name="IntakeAgent",
            input_hash=input_hash,
            output_fields={"trace_id": trace_id},
            latency_ms=(time.time() - start_time) * 1000,
            status="success"
        )
        return ctx

class FraudAgent:
    def __init__(self):
        self.rule_engine = RuleEngine()
        
    async def execute(self, ctx: ClaimContext) -> dict:
        start_time = time.time()
        input_hash = hashlib.md5(ctx.raw_input.model_dump_json().encode()).hexdigest()
        
        # Realism Update: NLP + Heuristics + Breakdowns
        fraud_score = 0.05
        breakdown = {}
        trace = []
        
        desc = ctx.raw_input.description.lower()
        if "staged" in desc or "suspicious" in desc:
            fraud_score += 0.4
            breakdown["NLP Keywords"] = 0.4
            trace.append("RULE_002_SUSPICIOUS_KEYWORD: Description contains flagged terminology.")
            
        if ctx.raw_input.claimAmount > 5000:
            val = min(0.3, ctx.raw_input.claimAmount / 50000.0)
            fraud_score += val
            breakdown["Amount Severity"] = round(val, 2)
            
        if ctx.raw_input.claimHistoryCount > 1:
            val = min(0.2, ctx.raw_input.claimHistoryCount * 0.05)
            fraud_score += val
            breakdown["Historical Frequency"] = round(val, 2)
            
        return {"fraud_score": min(fraud_score, 1.0), "fraud_breakdown": breakdown, "decision_trace": trace}

class SeverityAgent:
    def __init__(self):
        self.rule_engine = RuleEngine()
        
    async def execute(self, ctx: ClaimContext) -> dict:
        start_time = time.time()
        input_hash = hashlib.md5(ctx.raw_input.model_dump_json().encode()).hexdigest()
        
        try:
            _, severity_score, _ = self.rule_engine.evaluate(ctx.raw_input)
            status = "success"
        except Exception:
            severity_score = 0.0
            status = "fallback"
            
        emit_log("SeverityAgent", input_hash, {"severity_score": severity_score}, (time.time() - start_time)*1000, status)
        return {"severity_score": severity_score}

class GraphAgent:
    def __init__(self):
        self.graph_engine = GraphIntelligenceEngine()
        
    async def execute(self, ctx: ClaimContext) -> dict:
        start_time = time.time()
        input_hash = hashlib.md5(ctx.raw_input.model_dump_json().encode()).hexdigest()
        
        async def run_graph():
            # Minimal simulated I/O bound to replicate Graph extraction block (Wait -> Resolve)
            global_graph_service.add_claim_entities(
                claim_id=ctx.raw_input.policyId, 
                person_id=ctx.raw_input.policyholderId, 
                vehicle_vin=ctx.raw_input.vehicleVin
            )
            return self.graph_engine.evaluate_risk(global_graph_service.get_graph(), ctx.raw_input.policyId)
            
        try:
            # Mandated rigid performance timeout
            graph_risk, graph_signals = await asyncio.wait_for(run_graph(), timeout=0.100)
            status = "success"
        except asyncio.TimeoutError:
            graph_risk = 0.5
            graph_signals = ["[GRAPH_AGENT] Timeout: Neutral fallback applied"]
            status = "fallback"
        except Exception:
            graph_risk = 0.0
        signals = []
        breakdown = {}
        
        # 1. Contagion from Policyholder
        if ctx.raw_input.policyholderId in global_graph_service.flagged_nodes:
            risk_bump = 0.4
            graph_risk += risk_bump
            breakdown["Policyholder Node Flagged"] = risk_bump
            signals.append("High claim frequency on person")
            
        # 2. Contagion from Vehicle
        if ctx.raw_input.vehicleVin in global_graph_service.flagged_nodes:
            risk_bump = 0.6
            graph_risk += risk_bump
            breakdown["Target Vehicle Flagged"] = risk_bump
            signals.append("Shared vehicle across 2 claimants")
            
        return {"graph_risk_score": min(graph_risk, 1.0), "graph_breakdown": breakdown, "graph_signals": signals}
