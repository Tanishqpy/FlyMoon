from fastapi import FastAPI, Request
from pydantic import BaseModel
from typing import Dict, Any, Optional, List
from mcp_env import MCPEnvironment

app = FastAPI()
env = MCPEnvironment()

class ActionRequest(BaseModel):
    type: str
    agent_id: Optional[str] = None
    target_id: Optional[str] = None
    target: Optional[Dict[str, Any]] = None
    resource_type: Optional[str] = None
    amount: Optional[int] = None
    message: Optional[Dict[str, Any]] = None
    data: Optional[Dict[str, Any]] = None
    agent_type: Optional[str] = None

@app.post("/step")
async def step(req: ActionRequest):
    # Convert Pydantic model to dict
    action = req.dict(exclude_none=True)
    return env.step(action)

@app.get("/reset")
def reset():
    return env.reset()

@app.get("/")
def root():
    return {"msg": "MCP is online", "version": "1.0", "status": "operational"}

@app.get("/state")
def get_state():
    return {"state": env.state}

@app.get("/actions")
def get_actions():
    return {"available_actions": env.available_actions}