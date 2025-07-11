import requests
import time
import os

# Configuration
SERVER_URL = os.environ.get("FLYMOON_SERVER_URL", "http://localhost:8000")  # Can be overridden via environment variable
AGENT_ID = "explorer_bot"
AGENT_TYPE = "scout"

# Register agent
print(f"Registering agent {AGENT_ID}...")
response = requests.post(f"{SERVER_URL}/step", json={
    "type": "register",
    "agent_id": AGENT_ID,
    "agent_type": AGENT_TYPE
})
print(f"Registration response: {response.json()}")

# Simple agent loop
for i in range(5):
    print(f"\n--- Step {i+1} ---")
    
    # Move toward resource
    move_x = i * 2  # Simple movement pattern
    move_y = i
    print(f"Moving to position ({move_x}, {move_y})...")
    response = requests.post(f"{SERVER_URL}/step", json={
        "type": "move",
        "agent_id": AGENT_ID,
        "target": {"x": move_x, "y": move_y}
    })
    print(f"Move response: {response.json()['result']}")
    
    # Observe surroundings
    print("Observing surroundings...")
    response = requests.post(f"{SERVER_URL}/step", json={
        "type": "observe",
        "agent_id": AGENT_ID
    })
    print(f"Observation: {response.json()['result']}")
    
    time.sleep(1)  # Wait between actions