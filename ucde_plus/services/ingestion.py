from models.schemas import FNOLRequest, FNOLResponse
from services.rule_engine import RuleEngine
from services.graph_builder import global_graph_service
from services.graph_intelligence import GraphIntelligenceEngine
from services.rl_engine import RLEngine

class IngestionPipeline:
    def __init__(self):
        self.rule_engine = RuleEngine()
        self.graph_engine = GraphIntelligenceEngine()
        self.rl_engine = RLEngine()

    def process_claim(self, request: FNOLRequest) -> FNOLResponse:
        # Phase 2 Rules
        fraud_score, severity_score, trace = self.rule_engine.evaluate(request)
        
        # Phase 3 Graph
        global_graph_service.add_claim_entities(
            claim_id=request.policyId, 
            person_id=request.policyholderId, 
            vehicle_vin=request.vehicleVin
        )
        
        graph_risk, graph_signals = self.graph_engine.evaluate_risk(
            global_graph_service.get_graph(), 
            request.policyId
        )
        
        # Output Baseline A/B evaluation explicitly
        if fraud_score > 0.5 or severity_score > 0.8 or graph_risk > 0.4:
            baseline_decision = "INVESTIGATE"
        else:
            baseline_decision = "AUTO_APPROVE"
            
        # RL Model Prediction over 6-Vector State
        rl_decision, expected_reward = self.rl_engine.predict(
            severity_score=severity_score,
            fraud_score=fraud_score,
            graph_risk=graph_risk,
            claim_amount=request.claimAmount,
            history_count=request.claimHistoryCount,
            time_since=request.timeSinceLastClaim
        )
        
        trace.append(f"A/B_COMPARISON: Baseline=[{baseline_decision}] | RL=[{rl_decision}]")
        
        # Enforce memory based on RL output
        if rl_decision == "INVESTIGATE":
            global_graph_service.mark_node_risk(request.policyId, True)
            if fraud_score > 0.5:
                if request.policyholderId: global_graph_service.mark_node_risk(request.policyholderId, True)
                if request.vehicleVin: global_graph_service.mark_node_risk(request.vehicleVin, True)
            
        if not trace:
            trace.append("RULE_000_CLEAN: No baseline rules violated.")
            
        return FNOLResponse(
            baselineDecision=baseline_decision,
            rlDecision=rl_decision,
            expectedReward=expected_reward,
            confidence=0.88,
            graphRisk=graph_risk,
            fraudScore=fraud_score,
            decisionTrace=trace,
            graphSignals=graph_signals
        )
