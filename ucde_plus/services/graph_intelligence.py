import networkx as nx
from typing import Tuple, List

class GraphIntelligenceEngine:
    def evaluate_risk(self, graph: nx.DiGraph, claim_id: str) -> Tuple[float, List[str]]:
        graph_risk = 0.0
        signals = []
        
        if not graph.has_node(claim_id):
            return graph_risk, signals

        # Scoring Weights
        W_SHARED = 0.3
        W_DENSITY = 0.2
        W_PROPAGATION = 0.4
        
        shared_entity_score = 0.0
        claim_density_score = 0.0
        neighbor_risk_score = 0.0
        
        # We find entities involved in this claim directly (Claim -> Person/Vehicle)
        entities = list(graph.successors(claim_id))
        
        for entity in entities:
            entity_data = graph.nodes[entity]
            entity_type = entity_data.get("type", "UNKNOWN")
            claim_count = entity_data.get("claim_count", 0)
            
            # Find all claims attached to this entity
            related_claims = list(graph.predecessors(entity))
            
            # Signal 1: Shared Entity Risk (Multi-person vehicle usage)
            if entity_type == "VEHICLE" and len(related_claims) > 1:
                filers = set()
                for c in related_claims:
                    for ce in graph.successors(c):
                        if graph.nodes[ce].get("type") == "PERSON":
                            filers.add(ce)
                if len(filers) > 1:
                    shared_entity_score += 1.0
                    signals.append(f"Shared vehicle across {len(filers)} claimants")

            # Signal 2: Repeat Claim Density
            if claim_count > 1:
                claim_density_score += 1.0
                signals.append(f"High claim frequency on {entity_type.lower()}")
            
            # Signal 3: Risk Propagation (Neighbor risk states)
            if entity_data.get("risk_flag"):
                neighbor_risk_score += 1.0
                signals.append("Direct connection to flagged node")
                
            for related_claim in related_claims:
                if related_claim != claim_id and graph.nodes[related_claim].get("risk_flag"):
                    neighbor_risk_score += 1.0
                    msg = "Linked to flagged historical claim"
                    if msg not in signals:
                        signals.append(msg)

        # Aggregate final graph logic
        graph_risk = (
            W_SHARED * shared_entity_score +
            W_DENSITY * claim_density_score +
            W_PROPAGATION * neighbor_risk_score
        )
        
        return min(1.0, graph_risk), signals
