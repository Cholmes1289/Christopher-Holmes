import uuid
from datetime import datetime
from typing import List, Dict, Any, Optional

class GraphNode:
    def __init__(self, id: str, type: str, content: Dict[str, Any], owner: str):
        self.id = id
        self.type = type
        self.content = content
        self.owner = owner
        self.created_at = datetime.now()
        self.version = 1
        self.history = []

class DigitalBackboneEngine:
    """
    A simulated Graph-Document engine representing SurrealDB.
    Handles RLS, Graph Relationships, and Versioning.
    """
    def __init__(self):
        self.nodes: Dict[str, GraphNode] = {}
        self.edges: List[Dict[str, str]] = []
        self.audit_log = []

    def create_node(self, type: str, content: Dict[str, Any], owner: str, actor: str) -> str:
        node_id = f"{type}:{uuid.uuid4()}"
        node = GraphNode(node_id, type, content, owner)
        self.nodes[node_id] = node
        self._log_action("CREATE", node_id, actor, content)
        return node_id

    def update_node(self, node_id: str, new_content: Dict[str, Any], actor: str) -> bool:
        if node_id not in self.nodes:
            return False

        node = self.nodes[node_id]
        # Snapshot for history
        node.history.append({
            "version": node.version,
            "content": node.content.copy(),
            "updated_at": datetime.now(),
            "updated_by": actor
        })

        node.content.update(new_content)
        node.version += 1
        self._log_action("UPDATE", node_id, actor, new_content)
        return True

    def connect(self, source_id: str, target_id: str, relation: str, actor: str):
        if source_id in self.nodes and target_id in self.nodes:
            edge = {"in": source_id, "out": target_id, "type": relation}
            self.edges.append(edge)
            self._log_action("CONNECT", f"{source_id}->{target_id}", actor, {"relation": relation})

    def query_with_rls(self, actor: str, role: str) -> List[Dict[str, Any]]:
        """
        Simulates Row-Level Security (RLS).
        Only owners or admins can see nodes.
        """
        results = []
        for node_id, node in self.nodes.items():
            if role == "admin" or node.owner == actor:
                results.append({
                    "id": node.id,
                    "type": node.type,
                    "content": node.content,
                    "owner": node.owner,
                    "version": node.version,
                    "created_at": node.created_at.isoformat()
                })
        return results

    def _log_action(self, action: str, resource: str, actor: str, details: Dict[str, Any]):
        entry = {
            "timestamp": datetime.now().isoformat(),
            "action": action,
            "resource": resource,
            "actor": actor,
            "details": details
        }
        self.audit_log.append(entry)

# Global engine instance
engine = DigitalBackboneEngine()

# Seed data
admin_id = "user:admin"
engine.create_node("source", {"name": "Finance API", "status": "active"}, admin_id, admin_id)
engine.create_node("process", {"name": "Tax Calculator", "logic": "v1.2"}, admin_id, admin_id)
