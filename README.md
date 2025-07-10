# MCP Server Client

A Python client library for interacting with the MCP Server. This library provides a simple wrapper around the MCP Server API to register agents, move them around, and observe the environment.

## Installation

1. Clone this repository:
```bash
git clone https://github.com/Tanishqpy/FlyMoon
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

MIT License

Copyright (c) 2025 Tanishq 

Permission is hereby granted, free of charge, to any person obtaining a copy
of this software and associated documentation files (the "Software"), to deal
in the Software without restriction, including without limitation the rights
to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
copies of the Software, and to permit persons to whom the Software is
furnished to do so, subject to the following conditions:

The above copyright notice and this permission notice shall be included in all
copies or substantial portions of the Software.

THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
SOFTWARE.
