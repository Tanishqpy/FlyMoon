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
                                 Apache License
                           Version 2.0, January 2004
                        http://www.apache.org/licenses/

   TERMS AND CONDITIONS FOR USE, REPRODUCTION, AND DISTRIBUTION

   1. Definitions.

      "License" shall mean the terms and conditions for use, reproduction,
      and distribution as defined by Sections 1 through 9 of this document.

      "Licensor" shall mean the copyright owner or entity authorized by
      the copyright owner that is granting the License.

      "Legal Entity" shall mean the union of the acting entity and all
      other entities that control, are controlled by, or are under common
      control with that entity. For the purposes of this definition,
      "control" means (i) the power, direct or indirect, to cause the
      direction or management of such entity, whether by contract or
      otherwise, or (ii) ownership of fifty percent (50%) or more of the
      outstanding shares, or (iii) beneficial ownership of such entity.

      "You" (or "Your") shall mean an individual or Legal Entity
      exercising permissions granted by this License.

      "Source" form shall mean the preferred form for making modifications,
      including but not limited to software source code, documentation
      source, and configuration files.

      "Object" form shall mean any form resulting from mechanical
      transformation or translation of a Source form, including but
      not limited to compiled object code, generated documentation,
      and conversions to other media types.

      "Work" shall mean the work of authorship, whether in Source or
      Object form, made available under the License, as indicated by a
      copyright notice that is included in or attached to the work
      (an example is provided in the Appendix below).

      "Derivative Works" shall mean any work, whether in Source or Object
      form, that is based on (or derived from) the Work and for which the
      editorial revisions, annotations, elaborations, or other modifications
      represent, as a whole, an original work of authorship. For the purposes
      of this License, Derivative Works shall not include works that remain
      separable from, or merely link (or bind by name) to the interfaces of,
      the Work and Derivative Works thereof.

      "Contribution" shall mean any work of authorship, including
      the original version of the Work and any modifications or additions
      to that Work or Derivative Works thereof, that is intentionally
      submitted to Licensor for inclusion in the Work by the copyright owner
      or by an individual or Legal Entity authorized to submit on behalf of
      the copyright owner. For the purposes of this definition, "submitted"
      means any form of electronic, verbal, or written communication sent
      to the Licensor or its representatives, including but not limited to
      communication on electronic mailing lists, source code control systems,
      and issue tracking systems that are managed by, or on behalf of, the
      Licensor for the purpose of discussing and improving the Work, but
      excluding communication that is conspicuously marked or otherwise
      designated in writing by the copyright owner as "Not a Contribution."

      "Contributor" shall mean Licensor and any individual or Legal Entity
      on behalf of whom a Contribution has been received by Licensor and
      subsequently incorporated within the Work.

   2. Grant of Copyright License. Subject to the terms and conditions of
      this License, each Contributor hereby grants to You a perpetual,
      worldwide, non-exclusive, no-charge, royalty-free, irrevocable
      copyright license to reproduce, prepare Derivative Works of,
      publicly display, publicly perform, sublicense, and distribute the
      Work and such Derivative Works in Source or Object form.

   3. Grant of Patent License. Subject to the terms and conditions of
      this License, each Contributor hereby grants to You a perpetual,
      worldwide, non-exclusive, no-charge, royalty-free, irrevocable
      (except as stated in this section) patent license to make, have made,
      use, offer to sell, sell, import, and otherwise transfer the Work,
      where such license applies only to those patent claims licensable
      by such Contributor that are necessarily infringed by their
      Contribution(s) alone or by combination of their Contribution(s)
      with the Work to which such Contribution(s) was submitted. If You
      institute patent litigation against any entity (including a
      cross-claim or counterclaim in a lawsuit) alleging that the Work
      or a Contribution incorporated within the Work constitutes direct
      or contributory patent infringement, then any patent licenses
      granted to You under this License for that Work shall terminate
      as of the date such litigation is filed.

   4. Redistribution. You may reproduce and distribute copies of the
      Work or Derivative Works thereof in any medium, with or without
      modifications, and in Source or Object form, provided that You
      meet the following conditions:

      (a) You must give any other recipients of the Work or
          Derivative Works a copy of this License; and

      (b) You must cause any modified files to carry prominent notices
          stating that You changed the files; and

      (c) You must retain, in the Source form of any Derivative Works
          that You distribute, all copyright, patent, trademark, and
          attribution notices from the Source form of the Work,
          excluding those notices that do not pertain to any part of
          the Derivative Works; and

      (d) If the Work includes a "NOTICE" text file as part of its
          distribution, then any Derivative Works that You distribute must
          include a readable copy of the attribution notices contained
          within such NOTICE file, excluding those notices that do not
          pertain to any part of the Derivative Works, in at least one
          of the following places: within a NOTICE text file distributed
          as part of the Derivative Works; within the Source form or
          documentation, if provided along with the Derivative Works; or,
          within a display generated by the Derivative Works, if and
          wherever such third-party notices normally appear. The contents
          of the NOTICE file are for informational purposes only and
          do not modify the License. You may add Your own attribution
          notices within Derivative Works that You distribute, alongside
          or as an addendum to the NOTICE text from the Work, provided
          that such additional attribution notices cannot be construed
          as modifying the License.

      You may add Your own copyright statement to Your modifications and
      may provide additional or different license terms and conditions
      for use, reproduction, or distribution of Your modifications, or
      for any such Derivative Works as a whole, provided Your use,
      reproduction, and distribution of the Work otherwise complies with
      the conditions stated in this License.

   5. Submission of Contributions. Unless You explicitly state otherwise,
      any Contribution intentionally submitted for inclusion in the Work
      by You to the Licensor shall be under the terms and conditions of
      this License, without any additional terms or conditions.
      Notwithstanding the above, nothing herein shall supersede or modify
      the terms of any separate license agreement you may have executed
      with Licensor regarding such Contributions.

   6. Trademarks. This License does not grant permission to use the trade
      names, trademarks, service marks, or product names of the Licensor,
      except as required for reasonable and customary use in describing the
      origin of the Work and reproducing the content of the NOTICE file.

   7. Disclaimer of Warranty. Unless required by applicable law or
      agreed to in writing, Licensor provides the Work (and each
      Contributor provides its Contributions) on an "AS IS" BASIS,
      WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or
      implied, including, without limitation, any warranties or conditions
      of TITLE, NON-INFRINGEMENT, MERCHANTABILITY, or FITNESS FOR A
      PARTICULAR PURPOSE. You are solely responsible for determining the
      appropriateness of using or redistributing the Work and assume any
      risks associated with Your exercise of permissions under this License.

   8. Limitation of Liability. In no event and under no legal theory,
      whether in tort (including negligence), contract, or otherwise,
      unless required by applicable law (such as deliberate and grossly
      negligent acts) or agreed to in writing, shall any Contributor be
      liable to You for damages, including any direct, indirect, special,
      incidental, or consequential damages of any character arising as a
      result of this License or out of the use or inability to use the
      Work (including but not limited to damages for loss of goodwill,
      work stoppage, computer failure or malfunction, or any and all
      other commercial damages or losses), even if such Contributor
      has been advised of the possibility of such damages.

   9. Accepting Warranty or Additional Liability. While redistributing
      the Work or Derivative Works thereof, You may choose to offer,
      and charge a fee for, acceptance of support, warranty, indemnity,
      or other liability obligations and/or rights consistent with this
      License. However, in accepting such obligations, You may act only
      on Your own behalf and on Your sole responsibility, not on behalf
      of any other Contributor, and only if You agree to indemnify,
      defend, and hold each Contributor harmless for any liability
      incurred by, or claims asserted against, such Contributor by reason
      of your accepting any such warranty or additional liability.

   END OF TERMS AND CONDITIONS

   APPENDIX: How to apply the Apache License to your work.

      To apply the Apache License to your work, attach the following
      boilerplate notice, with the fields enclosed by brackets "[]"
      replaced with your own identifying information. (Don't include
      the brackets!)  The text should be enclosed in the appropriate
      comment syntax for the file format. We also recommend that a
      file or class name and description of purpose be included on the
      same "printed page" as the copyright notice for easier
      identification within third-party archives.

   Copyright [yyyy] [name of copyright owner]

   Licensed under the Apache License, Version 2.0 (the "License");
   you may not use this file except in compliance with the License.
   You may obtain a copy of the License at

       http://www.apache.org/licenses/LICENSE-2.0

   Unless required by applicable law or agreed to in writing, software
   distributed under the License is distributed on an "AS IS" BASIS,
   WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
   See the License for the specific language governing permissions and
   limitations under the License.
