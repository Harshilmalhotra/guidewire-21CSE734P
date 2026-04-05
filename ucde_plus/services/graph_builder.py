import networkx as nx

class GraphRepository:
    def save_snapshot(self):
        # Stub for saving state to Neo4j / Document DB
        pass

    def load_snapshot(self):
        # Stub for loading state from persistent storage
        pass

class GraphService:
    def __init__(self):
        self.graph = nx.DiGraph() # Using DiGraph to enforce directional edges
        self.repository = GraphRepository()

    def add_claim_entities(self, claim_id: str, person_id: str, vehicle_vin: str):
        # Claim Node
        if not self.graph.has_node(claim_id):
            self.graph.add_node(claim_id, type="CLAIM", risk_flag=False, claim_count=1)
        
        # Person Node
        if person_id:
            if not self.graph.has_node(person_id):
                self.graph.add_node(person_id, type="PERSON", risk_flag=False, claim_count=0)
            self.graph.nodes[person_id]["claim_count"] += 1
            self.graph.add_edge(claim_id, person_id, type="FILED_BY")
            
        # Vehicle Node
        if vehicle_vin:
            if not self.graph.has_node(vehicle_vin):
                self.graph.add_node(vehicle_vin, type="VEHICLE", risk_flag=False, claim_count=0)
            self.graph.nodes[vehicle_vin]["claim_count"] += 1
            self.graph.add_edge(claim_id, vehicle_vin, type="INVOLVES")

    def mark_node_risk(self, node_id: str, is_risky: bool = True):
        if self.graph.has_node(node_id) and node_id is not None:
            self.graph.nodes[node_id]["risk_flag"] = is_risky

    def get_graph(self) -> nx.DiGraph:
        return self.graph

# Singleton instance for in-memory persistence
# Thread-safe note: For production concurrency, wrapping modifications with locks is recommended.
global_graph_service = GraphService()
