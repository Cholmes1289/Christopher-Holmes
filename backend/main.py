from fastapi import FastAPI, HTTPException, Header, Depends
from pydantic import BaseModel
from typing import List, Optional, Dict, Any
import os
import uuid
from datetime import datetime
from fastapi.middleware.cors import CORSMiddleware

# --- Simulated Graph Engine (SurrealDB Mock) ---
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
    def __init__(self):
        self.nodes: Dict[str, GraphNode] = {}
        self.audit_log = []

    def create_node(self, type: str, content: Dict[str, Any], owner: str, actor: str) -> str:
        node_id = f"{type}:{uuid.uuid4()}"
        node = GraphNode(node_id, type, content, owner)
        self.nodes[node_id] = node
        self._log_action("CREATE", node_id, actor, content)
        return node_id

    def query_with_rls(self, actor: str, role: str) -> List[Dict[str, Any]]:
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
        self.audit_log.append({
            "timestamp": datetime.now().isoformat(),
            "action": action,
            "resource": resource,
            "actor": actor,
            "details": details
        })

engine = DigitalBackboneEngine()
engine.create_node("source", {"name": "Finance API", "status": "active"}, "user:admin", "user:admin")
engine.create_node("process", {"name": "Tax Calculator", "logic": "v1.2"}, "user:admin", "user:admin")

# --- API Layer ---
app = FastAPI(title="Flux-Lang | Digital Backbone API")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

def get_current_user(authorization: str = Header(None)):
    if not authorization or not authorization.startswith("Bearer "):
        raise HTTPException(status_code=401, detail="Unauthorized")
    token = authorization.split(" ")[1]
    if token == "admin-token":
        return {"id": "user:admin", "role": "admin"}
    return {"id": f"user:{token[:8]}", "role": "user"}

@app.get("/")
async def root():
    return {"status": "online", "platform": "Flux-Lang Digital Backbone"}

@app.get("/nodes")
async def get_nodes(user: dict = Depends(get_current_user)):
    return engine.query_with_rls(user["id"], user["role"])

@app.get("/audit")
async def get_audit(user: dict = Depends(get_current_user)):
    if user["role"] != "admin":
        raise HTTPException(status_code=403, detail="Forbidden")
    return engine.audit_log

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)
