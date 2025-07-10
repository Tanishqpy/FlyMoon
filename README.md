# MCP Server Client

A Python client library for interacting with the MCP Server. This library provides a simple wrapper around the MCP Server API to register agents, move them around, and observe the environment.

## Installation

1. Clone this repository:
```bash
git clone <repository-url>
cd <repository-directory>
```

2. Install the required dependencies:
```bash
pip install -r requirements.txt
```

## Usage

### Basic Usage

```python
from mcp_client import MCPClient

# Create a client instance
client = MCPClient(
    server_url="http://localhost:8000",
    agent_id="explorer_bot",
    agent_type="scout"
)

# Register the agent
registration_result = client.register()
print(f"Registration result: {registration_result}")

# Move the agent
move_result = client.move(x=10, y=5)
print(f"Move result: {move_result}")

# Observe surroundings
observation = client.observe()
print(f"Observation: {observation}")
```

### Automated Agent Loop

The client also includes a simple automation function:

```python
# Run a simple agent loop (5 steps by default)
client = MCPClient(agent_id="explorer_bot", agent_type="scout")
client.run_simple_loop(steps=5, delay=1)
```

## API Reference

### MCPClient

#### Constructor
- `MCPClient(server_url="http://localhost:8000", agent_id=None, agent_type=None)`

#### Methods
- `register(agent_id=None, agent_type=None)`: Register an agent with the server
- `move(x, y)`: Move the agent to the specified coordinates
- `observe()`: Observe the surroundings
- `run_simple_loop(steps=5, delay=1)`: Run an automated agent loop

## Example Agent

See `agent_client.py` for a simple example of directly using the API without the wrapper.

## License

[Insert your license information here]