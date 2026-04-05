import networkx as nx
from typing import Tuple, List

class GraphIntelligenceEngine:
    def evaluate_risk(self, graph: nx.Graph, claim_id: str) -> Tuple[float, List[str]]:
        graph_risk = 0.10  # Base logic
        trace = []
        
        if claim_id not in graph:
            return graph_risk, trace
            
        # Evaluate 1-hop and 2-hop neighbors for anomalies
        # High degree centrality on entities (like multiple claims on one VIN) increases risk
        
        connected_entities = list(graph.neighbors(claim_id))
        
        for entity in connected_entities:
            # entity could be a VEHICLE or POLICYHOLDER
            entity_attributes = graph.nodes[entity]
            
            # Check how many claims are attached to this entity
            entity_claims = [n for n in graph.neighbors(entity) if graph.nodes[n].get("type") == "CLAIM"]
            
            if len(entity_claims) > 1:
                # E.g. Multiple claims linked to the same VIN or Policyholder
                graph_risk += 0.30
                trace.append(f"RULE_003_GRAPH_ANOMALY: Entity '{entity}' linked to multiple claims: {entity_claims}")
        
        # Enforce bounds
        graph_risk = min(1.0, graph_risk)
        return graph_risk, trace
