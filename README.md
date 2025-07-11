# FlyMoon - MCP Server and Client

A Python package for both the MCP (Mission Control Protocol) Server and Client. This library provides a server implementation for agent simulations and a simple client wrapper around the MCP Server API to register agents, move them around, and observe the environment.

## Table of Contents
- [Installation](#installation)
- [Usage](#usage)
  - [Client Usage](#client-usage)
  - [Server Usage](#server-usage)
  - [Automated Agent Loop](#automated-agent-loop)
- [API Reference](#api-reference)
  - [Client API](#client-api)
  - [Server API](#server-api)
- [Project Structure](#project-structure)
- [Example Agent](#example-agent)
- [Troubleshooting](#troubleshooting)
- [Contributing](#contributing)
- [License](#license)

## Installation

### Option 1: Install from PyPI (Recommended)
```bash
pip install flymoon
```

### Option 2: Install from Source
1. Clone this repository:
```bash
git clone https://github.com/Tanishqpy/FlyMoon
cd FlyMoon
pip install -e .
```

2. Install the required dependencies:
```bash
pip install -r requirements.txt
```

3. (Optional) Create a virtual environment:
```bash
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
```

## Usage

### Client Usage

```python
from flymoon import MCPClient

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

### Server Usage

```python
from flymoon.server import start_server

# Start the server on default host and port (0.0.0.0:8000)
start_server()

# Or specify custom host and port
start_server(host="127.0.0.1", port=9000)
```

The server can also be started directly from the command line:

```bash
# Using the module
python -m flymoon.server

# Or if installed as a package
python -c "from flymoon.server import start_server; start_server()"
```

### Automated Agent Loop

The client also includes a simple automation function:

```python
# Run a simple agent loop (5 steps by default)
client = MCPClient(agent_id="explorer_bot", agent_type="scout")
client.run_simple_loop(steps=5, delay=1)
```

## API Reference

### Client API

#### MCPClient

##### Constructor
- `MCPClient(server_url="http://localhost:8000", agent_id=None, agent_type=None)`

##### Methods
- `register(agent_id=None, agent_type=None)`: Register an agent with the server
- `move(x, y)`: Move the agent to the specified coordinates
- `observe()`: Observe the surroundings
- `run_simple_loop(steps=5, delay=1)`: Run an automated agent loop

### Server API

#### Endpoints

- `GET /`: Check if the server is running
- `POST /step`: Main endpoint for agent actions

#### Step Request Types

1. **Register**
   ```json
   {
     "type": "register",
     "agent_id": "unique_agent_id",
     "agent_type": "scout"
   }
   ```

2. **Move**
   ```json
   {
     "type": "move",
     "agent_id": "unique_agent_id",
     "target": {"x": 10, "y": 20}
   }
   ```

3. **Observe**
   ```json
   {
     "type": "observe",
     "agent_id": "unique_agent_id"
   }
   ```

#### Server Functions

- `start_server(host="0.0.0.0", port=8000)`: Start the MCP server

## Project Structure

- `src/FlyMoon/`
  - `__init__.py`: Package initialization
  - `mcp_client.py`: Main client library class
  - `server.py`: FastAPI server implementation
  - `agent_client.py`: Example implementation without using the wrapper
  - `mcp_env.py`: Environment definition and functionality
- `launch_mcp.sh`: Script to start the server with ngrok tunneling
- `requirements.txt`: Project dependencies
- `pyproject.toml`: Project configuration

## Example Agent

See `agent_client.py` for a simple example of directly using the API without the wrapper.

## Troubleshooting

### Common Issues

1. **Connection refused errors**
   - Make sure the MCP server is running on the specified port
   - Check if the server URL is correct
   - Verify network connectivity

2. **Authentication failures**
   - Ensure you're using a valid agent_id
   - Try re-registering your agent

3. **Movement limitations**
   - Agents can't move outside the environment boundaries
   - Check observation results for valid movement ranges

### Server Setup

To start the server locally:

```bash
# Start the FastAPI server
uvicorn flymoon.server:app --reload

# Or use the provided launch script
./launch_mcp.sh
```

## Contributing

Contributions are welcome! Here's how you can contribute:

1. Fork the repository
2. Create a new branch (`git checkout -b feature/amazing-feature`)
3. Make your changes
4. Commit your changes (`git commit -m 'Add some amazing feature'`)
5. Push to the branch (`git push origin feature/amazing-feature`)
6. Open a Pull Request

Please make sure to update tests as appropriate.

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