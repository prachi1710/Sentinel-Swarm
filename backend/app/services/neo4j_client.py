import os
from neo4j import GraphDatabase

NEO4J_URI = os.getenv("NEO4J_URI", "bolt://localhost:7687")
NEO4J_USER = os.getenv("NEO4J_USER", "neo4j")
NEO4J_PASSWORD = os.getenv("NEO4J_PASSWORD", "sentinel-swarm-password")

class Neo4jClient:
    def __init__(self):
        self.driver = GraphDatabase.driver(NEO4J_URI, auth=(NEO4J_USER, NEO4J_PASSWORD))
        
    def close(self):
        self.driver.close()
        
    def log_interaction(self, user_id: str, agent_id: str, threat_detected: bool, threat_details: dict = None):
        """Log an interaction between a user and an agent, marking threats if any."""
        interaction_query = """
        MERGE (u:User {id: $user_id})
        MERGE (a:Agent {id: $agent_id})
        CREATE (u)-[r:INTERACTED_WITH {
            timestamp: datetime(), 
            threat_detected: $threat_detected,
            threat_type: $threat_type
        }]->(a)
        """
        
        status_query = """
        MATCH (a:Agent {id: $agent_id})
        SET a.status = CASE WHEN $threat_detected THEN "compromised" ELSE "safe" END
        """
        
        threat_type = threat_details.get("threat_type") if threat_details else "None"
        
        with self.driver.session() as session:
            session.run(interaction_query, user_id=user_id, agent_id=agent_id, 
                        threat_detected=threat_detected, threat_type=threat_type)
            session.run(status_query, agent_id=agent_id, threat_detected=threat_detected)

    def get_graph(self):
        """Retrieve nodes and edges for React Flow."""
        query = """
        MATCH (n)
        OPTIONAL MATCH (n)-[r]->(m)
        RETURN n, r, m
        """
        nodes = []
        edges = []
        node_ids = set()
        
        with self.driver.session() as session:
            result = session.run(query)
            for record in result:
                n = record["n"]
                if n and n.id not in node_ids:
                    status = dict(n).get("status", "safe")
                    nodes.append({"id": str(n.id), "label": dict(n).get("id", "Unknown"), "type": list(n.labels)[0], "status": status})
                    node_ids.add(n.id)
                
                m = record["m"]
                if m and m.id not in node_ids:
                    status = dict(m).get("status", "safe")
                    nodes.append({"id": str(m.id), "label": dict(m).get("id", "Unknown"), "type": list(m.labels)[0], "status": status})
                    node_ids.add(m.id)
                    
                r = record["r"]
                if r:
                    edges.append({"id": str(r.id), "source": str(r.nodes[0].id), "target": str(r.nodes[1].id), "type": r.type})
                    
        return {"nodes": nodes, "edges": edges}

neo4j_client = Neo4jClient()
