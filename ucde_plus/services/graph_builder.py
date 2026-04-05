import networkx as nx

class ClaimGraph:
    def __init__(self):
        self.graph = nx.Graph()

    def add_claim_entities(self, claim_id: str, policyholder_id: str, vehicle_vin: str):
        # Add primary claim node
        self.graph.add_node(claim_id, type="CLAIM")
        
        # Policyholder node
        if policyholder_id:
            self.graph.add_node(policyholder_id, type="POLICYHOLDER")
            self.graph.add_edge(claim_id, policyholder_id, relation="filed_by")
            
        # Vehicle node
        if vehicle_vin:
            self.graph.add_node(vehicle_vin, type="VEHICLE")
            self.graph.add_edge(claim_id, vehicle_vin, relation="involved_vehicle")

    def get_graph(self):
        return self.graph

# Singleton instance for in-memory persistence
global_claim_graph = ClaimGraph()
