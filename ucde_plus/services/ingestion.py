from models.schemas import FNOLRequest, FNOLResponse
from services.rule_engine import RuleEngine
from services.graph_builder import global_claim_graph
from services.graph_intelligence import GraphIntelligenceEngine

class IngestionPipeline:
    def __init__(self):
        self.rule_engine = RuleEngine()
        self.graph_engine = GraphIntelligenceEngine()

    def process_claim(self, request: FNOLRequest) -> FNOLResponse:
        # Phase 2: Rule-based Scoring Engine Evaluation
        fraud_score, severity_score, trace = self.rule_engine.evaluate(request)
        
        # Phase 3: Graph Layer Evaluation
        global_claim_graph.add_claim_entities(
            claim_id=request.policyId, 
            policyholder_id=request.policyholderId, 
            vehicle_vin=request.vehicleVin
        )
        
        graph_risk, graph_trace = self.graph_engine.evaluate_risk(
            global_claim_graph.get_graph(), 
            request.policyId
        )
        trace.extend(graph_trace)
        
        # Determine decision based on thresholds
        if fraud_score > 0.5 or severity_score > 0.8 or graph_risk > 0.2:
            decision = "INVESTIGATE"
            confidence = 0.85
        else:
            decision = "APPROVE"
            confidence = 0.95
            
        if not trace:
            trace.append("RULE_000_CLEAN: No baseline rules violated.")
            
        return FNOLResponse(
            decision=decision,
            confidence=confidence,
            graphRisk=graph_risk,
            fraudScore=fraud_score,
            decisionTrace=trace
        )
