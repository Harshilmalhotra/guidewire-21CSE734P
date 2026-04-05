from models.schemas import FNOLRequest, FNOLResponse
from services.rule_engine import RuleEngine
from services.graph_builder import global_graph_service
from services.graph_intelligence import GraphIntelligenceEngine

class IngestionPipeline:
    def __init__(self):
        self.rule_engine = RuleEngine()
        self.graph_engine = GraphIntelligenceEngine()

    def process_claim(self, request: FNOLRequest) -> FNOLResponse:
        # Phase 2: Rule-based Scoring Engine Evaluation
        fraud_score, severity_score, trace = self.rule_engine.evaluate(request)
        
        # Phase 3: Graph Layer Evaluation
        global_graph_service.add_claim_entities(
            claim_id=request.policyId, 
            person_id=request.policyholderId, 
            vehicle_vin=request.vehicleVin
        )
        
        graph_risk, graph_signals = self.graph_engine.evaluate_risk(
            global_graph_service.get_graph(), 
            request.policyId
        )
        
        # Determine decision based on thresholds
        # Notice we are checking either fraud bounds OR graph_risk triggers natively
        if fraud_score > 0.5 or severity_score > 0.8 or graph_risk > 0.4:
            decision = "INVESTIGATE"
            confidence = 0.85
            
            # Apply Risk Propagation Memory to nodes involved
            global_graph_service.mark_node_risk(request.policyId, True)
            if fraud_score > 0.5:
                # Substantial fraud causes systemic entity penalization
                if request.policyholderId: global_graph_service.mark_node_risk(request.policyholderId, True)
                if request.vehicleVin: global_graph_service.mark_node_risk(request.vehicleVin, True)
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
            decisionTrace=trace,
            graphSignals=graph_signals
        )
