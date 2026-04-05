import asyncio
from models.schemas import FNOLRequest, FNOLResponse
from models.state import ClaimContext
from services.agents import IntakeAgent, FraudAgent, SeverityAgent, GraphAgent
from services.rl_engine import RLEngine
from services.graph_builder import global_graph_service

class AggregationLayer:
    def extract_vector(self, ctx: ClaimContext) -> dict:
        """Isolated extraction isolating contextual mappings before hitting RL prediction blocks."""
        return {
            "severity_score": ctx.severity_score if ctx.severity_score is not None else 0.0,
            "fraud_score": ctx.fraud_score if ctx.fraud_score is not None else 0.0,
            "graph_risk": ctx.graph_risk_score if ctx.graph_risk_score is not None else 0.5,
            "claim_amount": ctx.raw_input.claimAmount,
            "history_count": ctx.raw_input.claimHistoryCount,
            "time_since": ctx.raw_input.timeSinceLastClaim
        }

class DecisionAgent:
    def __init__(self):
        self.rl_engine = RLEngine()
        
    def execute(self, vector: dict, ctx: ClaimContext) -> ClaimContext:
        # RL execution isolated logic
        rl_decision, expected_reward = self.rl_engine.predict(
            severity_score=vector["severity_score"],
            fraud_score=vector["fraud_score"],
            graph_risk=vector["graph_risk"],
            claim_amount=vector["claim_amount"],
            history_count=vector["history_count"],
            time_since=vector["time_since"]
        )
        
        # Baseline parity proxy evaluated distinctly
        if vector["fraud_score"] > 0.5 or vector["severity_score"] > 0.8 or vector["graph_risk"] > 0.4:
            baseline_decision = "INVESTIGATE"
        else:
            baseline_decision = "AUTO_APPROVE"
            
        trace = [f"A/B_COMPARISON: Baseline=[{baseline_decision}] | RL=[{rl_decision}]"]
        
        # Emit persistent node status dynamically over global graph proxy representing Memory logic bounds
        if rl_decision == "INVESTIGATE":
            global_graph_service.mark_node_risk(ctx.raw_input.policyId, True)
            if vector["fraud_score"] > 0.5:
                if ctx.raw_input.policyholderId: global_graph_service.mark_node_risk(ctx.raw_input.policyholderId, True)
                if ctx.raw_input.vehicleVin: global_graph_service.mark_node_risk(ctx.raw_input.vehicleVin, True)
                
        # Returns safe context mutation over established immutable limits
        return ctx.update(
            baseline_decision=baseline_decision,
            rl_decision=rl_decision,
            expected_reward=expected_reward,
            decision_trace=trace
        )

class AgenticOrchestrator:
    def __init__(self):
        self.intake = IntakeAgent()
        self.fraud = FraudAgent()
        self.severity = SeverityAgent()
        self.graph = GraphAgent()
        self.aggregator = AggregationLayer()
        self.decision = DecisionAgent()

    async def process(self, request: FNOLRequest) -> FNOLResponse:
        # DAG Execute: Intake -> Gather(Fraud, Severity, Graph) -> Merge -> Aggregation -> Decision
        
        # 1. Intake Layer (Synchronous validation setup)
        ctx = self.intake.execute(request)
        
        # 2. Parallel fan-out architecture
        results = await asyncio.gather(
            self.fraud.execute(ctx),
            self.severity.execute(ctx),
            self.graph.execute(ctx),
            return_exceptions=True
        )
        
        # 3. Aggregation merge barrier securing compile parity mapping dict combinations
        merge_data = {}
        for res in results:
            if isinstance(res, dict):
                for k, v in res.items():
                    merge_data[k] = v
        
        # Explicit deterministic Context creation
        ctx = ctx.update(**merge_data)
        
        # 4. Independent Aggregation format mapping decoupling RL Logic cleanly
        vector = self.aggregator.extract_vector(ctx)
        
        # 5. Core Decision logic loop
        ctx = self.decision.execute(vector, ctx)
        
        # Transform finalized immutable context explicitly back to standard generic FNOL API payload schema structure
        return FNOLResponse(
            baselineDecision=ctx.baseline_decision,
            rlDecision=ctx.rl_decision,
            expectedReward=ctx.expected_reward,
            confidence=0.88,
            graphRisk=ctx.graph_risk_score if ctx.graph_risk_score is not None else 0.5,
            fraudScore=ctx.fraud_score if ctx.fraud_score is not None else 0.0,
            decisionTrace=ctx.decision_trace,
            graphSignals=ctx.graph_signals
        )
