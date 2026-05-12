from fastapi import FastAPI, HTTPException, Header
from pydantic import BaseModel
from typing import List, Optional
import os
import uuid
from datetime import datetime
from fastapi.middleware.cors import CORSMiddleware

app = FastAPI(title="Flux-Lang Digital Backbone")
app.add_middleware(CORSMiddleware, allow_origins=["*"], allow_methods=["*"], allow_headers=["*"])

class Record(BaseModel):
    id: Optional[str] = None
    content: str
    owner: str
    created_at: Optional[str] = None

mock_db = [
    {"id": "record:1", "content": "Initial Data Source", "owner": "user:admin", "created_at": str(datetime.now())},
    {"id": "record:2", "content": "Project Alpha Details", "owner": "user:jules", "created_at": str(datetime.now())}
]

@app.get("/")
async def root():
    return {"message": "Welcome to the Flux-Lang Digital Backbone (Mock Mode)", "status": "online"}

@app.get("/records", response_model=List[Record])
async def get_records(authorization: str = Header(None)):
    if not authorization:
        raise HTTPException(status_code=401, detail="Unauthorized")
    return mock_db

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)
