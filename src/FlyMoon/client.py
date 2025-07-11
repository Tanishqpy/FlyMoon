import requests
import time
from requests.exceptions import RequestException, Timeout, ConnectionError

class MCPClient:
    """Client wrapper for MCP Server API interactions"""
    
    def __init__(self, server_url="http://localhost:8000", agent_id=None, agent_type=None, timeout=10):
        """Initialize the MCP Client with server URL and agent details"""
        self.server_url = server_url
        self.agent_id = agent_id
        self.agent_type = agent_type
        self.registered = False
        self.name = "FlyMoon Client"
        self.timeout = timeout
        self.session = requests.Session()  # Use session for connection pooling
    
    def _api_call(self, payload):
        """Internal method to handle API calls with error handling"""
        try:
            response = self.session.post(
                f"{self.server_url}/step", 
                json=payload,
                timeout=self.timeout
            )
            response.raise_for_status()  # Raise exception for 4XX/5XX responses
            return response.json()
        except Timeout:
            raise TimeoutError(f"Request to {self.server_url} timed out")
        except ConnectionError:
            raise ConnectionError(f"Failed to connect to {self.server_url}")
        except RequestException as e:
            raise RuntimeError(f"API request failed: {str(e)}")
        except ValueError:  # JSON parsing error
            raise ValueError(f"Invalid response format from server")
    
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
        
        result = self._api_call({
            "type": "register",
            "agent_id": agent_id,
            "agent_type": agent_type
        })
        
        self.registered = True
        return result
    
    def move(self, x, y):
        """Move agent to the specified coordinates"""
        if not self.registered:
            raise RuntimeError("Agent must be registered before moving")
        
        # Validate coordinates
        if not isinstance(x, (int, float)) or not isinstance(y, (int, float)):
            raise TypeError("Coordinates must be numeric values")
            
        return self._api_call({
            "type": "move",
            "agent_id": self.agent_id,
            "target": {"x": x, "y": y}
        })
    
    def observe(self):
        """Observe the surroundings"""
        if not self.registered:
            raise RuntimeError("Agent must be registered before observing")
            
        return self._api_call({
            "type": "observe",
            "agent_id": self.agent_id
        })
    
    def run_simple_loop(self, steps=5, delay=1):
        """Run a simple agent loop similar to the original script"""
        if not self.registered:
            print(f"Registering agent {self.agent_id}...")
            try:
                registration_result = self.register()
                print(f"Registration response: {registration_result}")
            except Exception as e:
                print(f"Registration failed: {str(e)}")
                return
        
        for i in range(steps):
            try:
                print(f"\n--- Step {i+1} ---")
                
                # Move toward resource
                move_x = i * 2  # Simple movement pattern
                move_y = i
                print(f"Moving to position ({move_x}, {move_y})...")
                move_result = self.move(move_x, move_y)
                print(f"Move response: {move_result.get('result', 'No result data')}")
                
                # Observe surroundings
                print("Observing surroundings...")
                observe_result = self.observe()
                print(f"Observation: {observe_result.get('result', 'No observation data')}")
                
                time.sleep(delay)  # Wait between actions
            except Exception as e:
                print(f"Error in step {i+1}: {str(e)}")
                # Continue with next step rather than terminating the loop
    
    def __del__(self):
        """Clean up resources when the client is destroyed"""
        if hasattr(self, 'session'):
            self.session.close()

# Example usage (if run directly)
if __name__ == "__main__":
    client = MCPClient(agent_id="explorer_bot", agent_type="scout")
    client.run_simple_loop()
