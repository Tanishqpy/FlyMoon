import requests
import time

class MCPClient:
    """Client wrapper for MCP Server API interactions"""
    
    def __init__(self, server_url="http://localhost:8000", agent_id=None, agent_type=None):
        """Initialize the MCP Client with server URL and agent details"""
        self.server_url = server_url
        self.agent_id = agent_id
        self.agent_type = agent_type
        self.registered = False
    
    def register(self, agent_id=None, agent_type=None):
        """Register an agent with the MCP Server"""
        # Use provided values or fallback to instance values
        agent_id = agent_id or self.agent_id
        agent_type = agent_type or self.agent_type
        
        if not agent_id or not agent_type:
            raise ValueError("Agent ID and type must be provided")
            
        # Update instance variables
        self.agent_id = agent_id
        self.agent_type = agent_type
        
        response = requests.post(f"{self.server_url}/step", json={
            "type": "register",
            "agent_id": agent_id,
            "agent_type": agent_type
        })
        
        result = response.json()
        self.registered = True
        return result
    
    def move(self, x, y):
        """Move agent to the specified coordinates"""
        if not self.registered:
            raise RuntimeError("Agent must be registered before moving")
            
        response = requests.post(f"{self.server_url}/step", json={
            "type": "move",
            "agent_id": self.agent_id,
            "target": {"x": x, "y": y}
        })
        
        return response.json()
    
    def observe(self):
        """Observe the surroundings"""
        if not self.registered:
            raise RuntimeError("Agent must be registered before observing")
            
        response = requests.post(f"{self.server_url}/step", json={
            "type": "observe",
            "agent_id": self.agent_id
        })
        
        return response.json()
    
    def run_simple_loop(self, steps=5, delay=1):
        """Run a simple agent loop similar to the original script"""
        if not self.registered:
            print(f"Registering agent {self.agent_id}...")
            registration_result = self.register()
            print(f"Registration response: {registration_result}")
        
        for i in range(steps):
            print(f"\n--- Step {i+1} ---")
            
            # Move toward resource
            move_x = i * 2  # Simple movement pattern
            move_y = i
            print(f"Moving to position ({move_x}, {move_y})...")
            move_result = self.move(move_x, move_y)
            print(f"Move response: {move_result['result']}")
            
            # Observe surroundings
            print("Observing surroundings...")
            observe_result = self.observe()
            print(f"Observation: {observe_result['result']}")
            
            time.sleep(delay)  # Wait between actions

# Example usage (if run directly)
if __name__ == "__main__":
    client = MCPClient(agent_id="explorer_bot", agent_type="scout")
    client.run_simple_loop()
