from fastapi import FastAPI, HTTPException
import uvicorn
from pydantic import BaseModel
from typing import Dict, Any, Optional
import logging

# Configure logging
logging.basicConfig(level=logging.INFO, 
                   format='%(asctime)s - %(name)s - %(levelname)s - %(message)s')
logger = logging.getLogger("mcp-server")

app = FastAPI(title="FlyMoon MCP Server")

# Store agents and world state
world_state = {
    "agents": {},
    "resources": {
        "resource1": {"x": 10, "y": 10, "type": "food"},
        "resource2": {"x": 20, "y": 5, "type": "water"}
    }
}

class StepRequest(BaseModel):
    type: str
    agent_id: str
    agent_type: Optional[str] = None
    target: Optional[Dict[str, float]] = None

@app.post("/step")
async def step(request: StepRequest):
    logger.info(f"Received request: {request}")
    
    if request.type == "register":
        # Register a new agent
        if not request.agent_type:
            raise HTTPException(status_code=400, detail="agent_type is required for registration")
        
        world_state["agents"][request.agent_id] = {
            "type": request.agent_type,
            "position": {"x": 0, "y": 0},
            "status": "active"
        }
        
        return {"result": f"Agent {request.agent_id} registered successfully", "status": "success"}
    
    # Validate agent exists for other operations
    if request.agent_id not in world_state["agents"]:
        raise HTTPException(status_code=404, detail=f"Agent {request.agent_id} not found")
    
    if request.type == "move":
        # Move the agent
        if not request.target:
            raise HTTPException(status_code=400, detail="target coordinates required for move")
        
        agent = world_state["agents"][request.agent_id]
        agent["position"] = request.target
        
        return {
            "result": f"Agent moved to position ({request.target['x']}, {request.target['y']})",
            "status": "success"
        }
    
    elif request.type == "observe":
        # Return surroundings
        agent_pos = world_state["agents"][request.agent_id]["position"]
        nearby_objects = []
        
        # Find nearby resources (simple distance check)
        for res_id, resource in world_state["resources"].items():
            dx = resource["x"] - agent_pos["x"]
            dy = resource["y"] - agent_pos["y"] 
            distance = (dx**2 + dy**2)**0.5
            
            if distance < 15:  # Within observable range
                nearby_objects.append({
                    "id": res_id,
                    "type": resource["type"],
                    "position": {"x": resource["x"], "y": resource["y"]},
                    "distance": distance
                })
        
        return {
            "result": {
                "position": agent_pos,
                "nearby_objects": nearby_objects
            },
            "status": "success"
        }
    
    else:
        raise HTTPException(status_code=400, detail=f"Unknown action type: {request.type}")

@app.get("/")
async def root():
    return {"message": "FlyMoon MCP Server is running"}

def start_server(host="0.0.0.0", port=8000):
    """Start the MCP server with the given host and port"""
    logger.info(f"Starting MCP server on {host}:{port}")
    uvicorn.run(app, host=host, port=port)

if __name__ == "__main__":
    start_server()
