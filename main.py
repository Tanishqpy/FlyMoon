from fastapi import FastAPI
from pydantic import BaseModel
from mcp_env import MCPEnvironment

app = FastAPI()
env = MCPEnvironment()

class ActionRequest(BaseModel):
    action: str

@app.post("/step")
def step(req: ActionRequest):
    return env.step(req.action)

@app.get("/reset")
def reset():
    return env.reset()

@app.get("/")
def root():
    return {"msg": "MCP is online"}
