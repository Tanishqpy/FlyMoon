class MCPEnvironment:
    def __init__(self):
        """Initialize the Multi-Agent Control Protocol environment."""
        # Environment state
        self.state = {
            "world_state": {
                "timestep": 0,
                "resources": {"energy": 100, "materials": 100},
                "locations": {
                    "base": {"x": 0, "y": 0},
                    "resource_1": {"x": 10, "y": 5},
                    "resource_2": {"x": -5, "y": 15}
                }
            },
            # Track all agents in the environment
            "agents": {}
        }
        
        # Available actions for agents
        self.available_actions = [
            "register", "move", "collect", "communicate", "process_data", 
            "transfer_resource", "observe"
        ]
        
        # History of agent interactions
        self.history = []

    def reset(self):
        """Reset the environment to its initial state."""
        self.__init__()
        return {
            "state": self.state,
            "message": "Environment reset successfully",
            "available_actions": self.available_actions
        }
    
    def step(self, action):
        """Process an agent action and update the environment."""
        # Record action in history
        self.history.append({
            "action": action,
            "timestep": self.state["world_state"]["timestep"]
        })
        
        # Process the action and get result
        result = self._process_action(action)
        
        # Update environment state (advance time, update resources, etc.)
        self._update_environment()
        
        return {
            "state": self.state,
            "result": result,
            "available_actions": self.available_actions
        }
    
    def _process_action(self, action):
        """Process the given action based on its type."""
        if isinstance(action, str):
            # Handle simple string actions for backward compatibility
            return {"success": False, "message": "Please provide structured action data"}
            
        if "type" not in action:
            return {"success": False, "message": "Action must specify a type"}
            
        action_type = action.get("type")
        agent_id = action.get("agent_id")
        
        # Validate action type
        if action_type not in self.available_actions:
            return {"success": False, "message": f"Unknown action type: {action_type}"}
            
        # Register new agent
        if action_type == "register":
            return self._register_agent(action)
            
        # Ensure the agent exists for other action types
        if agent_id not in self.state["agents"]:
            return {"success": False, "message": f"Unknown agent: {agent_id}"}
            
        # Handle different action types
        if action_type == "move":
            return self._handle_move(action)
        elif action_type == "collect":
            return self._handle_collect(action)
        elif action_type == "communicate":
            return self._handle_communicate(action)
        elif action_type == "process_data":
            return self._handle_process_data(action)
        elif action_type == "transfer_resource":
            return self._handle_transfer(action)
        elif action_type == "observe":
            return self._handle_observe(action)
        
        return {"success": False, "message": "Action handling not implemented"}

    def _register_agent(self, action):
        """Register a new agent in the environment."""
        agent_id = action.get("agent_id")
        agent_type = action.get("agent_type", "generic")
        
        if agent_id in self.state["agents"]:
            return {"success": False, "message": f"Agent {agent_id} already exists"}
            
        # Create new agent with default properties
        self.state["agents"][agent_id] = {
            "type": agent_type,
            "position": {"x": 0, "y": 0},
            "resources": {"energy": 100},
            "status": "active",
            "knowledge": {}
        }
        
        return {
            "success": True, 
            "message": f"Agent {agent_id} registered successfully",
            "agent_data": self.state["agents"][agent_id]
        }

    def _handle_move(self, action):
        """Handle agent movement."""
        agent_id = action.get("agent_id")
        target = action.get("target", {})
        
        # Get current position
        current_pos = self.state["agents"][agent_id]["position"]
        
        # Update position
        if "x" in target:
            current_pos["x"] = target["x"]
        if "y" in target:
            current_pos["y"] = target["y"]
            
        # Reduce energy based on movement
        self.state["agents"][agent_id]["resources"]["energy"] -= 5
        
        return {
            "success": True,
            "message": f"Agent {agent_id} moved to ({current_pos['x']}, {current_pos['y']})"
        }

    def _handle_collect(self, action):
        """Handle resource collection."""
        agent_id = action.get("agent_id")
        resource_type = action.get("resource_type", "energy")
        
        # Check if agent is near a resource
        agent_pos = self.state["agents"][agent_id]["position"]
        collected = False
        
        # Simple distance-based collection
        for loc_name, loc_pos in self.state["world_state"]["locations"].items():
            if "resource" in loc_name:
                distance = ((agent_pos["x"] - loc_pos["x"])**2 + 
                           (agent_pos["y"] - loc_pos["y"])**2)**0.5
                if distance < 2:  # If agent is close enough
                    collected = True
                    # Add resources to agent
                    if resource_type not in self.state["agents"][agent_id]["resources"]:
                        self.state["agents"][agent_id]["resources"][resource_type] = 0
                    self.state["agents"][agent_id]["resources"][resource_type] += 10
                    break
        
        if collected:
            return {
                "success": True,
                "message": f"Agent {agent_id} collected {resource_type}"
            }
        else:
            return {
                "success": False,
                "message": f"Agent {agent_id} is not near any resource"
            }

    def _handle_communicate(self, action):
        """Handle communication between agents."""
        agent_id = action.get("agent_id")
        target_id = action.get("target_id")
        message = action.get("message", {})
        
        if target_id not in self.state["agents"]:
            return {
                "success": False,
                "message": f"Target agent {target_id} doesn't exist"
            }
        
        # Add message to target agent's knowledge
        if "messages" not in self.state["agents"][target_id]["knowledge"]:
            self.state["agents"][target_id]["knowledge"]["messages"] = []
            
        self.state["agents"][target_id]["knowledge"]["messages"].append({
            "from": agent_id,
            "content": message,
            "timestep": self.state["world_state"]["timestep"]
        })
        
        return {
            "success": True,
            "message": f"Message sent from {agent_id} to {target_id}"
        }

    def _handle_process_data(self, action):
        """Handle data processing actions."""
        agent_id = action.get("agent_id")
        data = action.get("data", {})
        
        # Update agent's knowledge
        if "processed_data" not in self.state["agents"][agent_id]["knowledge"]:
            self.state["agents"][agent_id]["knowledge"]["processed_data"] = []
            
        self.state["agents"][agent_id]["knowledge"]["processed_data"].append({
            "data": data,
            "timestep": self.state["world_state"]["timestep"]
        })
        
        # Processing consumes energy
        self.state["agents"][agent_id]["resources"]["energy"] -= 3
        
        return {
            "success": True,
            "message": f"Agent {agent_id} processed data successfully"
        }

    def _handle_transfer(self, action):
        """Handle resource transfer between agents."""
        agent_id = action.get("agent_id")
        target_id = action.get("target_id")
        resource_type = action.get("resource_type", "energy")
        amount = action.get("amount", 0)
        
        if target_id not in self.state["agents"]:
            return {
                "success": False,
                "message": f"Target agent {target_id} doesn't exist"
            }
        
        # Check if source agent has enough resources
        if resource_type not in self.state["agents"][agent_id]["resources"] or \
           self.state["agents"][agent_id]["resources"][resource_type] < amount:
            return {
                "success": False,
                "message": f"Agent {agent_id} has insufficient {resource_type}"
            }
        
        # Ensure target agent has the resource type initialized
        if resource_type not in self.state["agents"][target_id]["resources"]:
            self.state["agents"][target_id]["resources"][resource_type] = 0
            
        # Transfer resources
        self.state["agents"][agent_id]["resources"][resource_type] -= amount
        self.state["agents"][target_id]["resources"][resource_type] += amount
        
        return {
            "success": True,
            "message": f"Transferred {amount} {resource_type} from {agent_id} to {target_id}"
        }

    def _handle_observe(self, action):
        """Handle observation actions."""
        agent_id = action.get("agent_id")
        
        # Get agent position
        agent_pos = self.state["agents"][agent_id]["position"]
        
        # What the agent can observe depends on its position
        observations = {
            "nearby_resources": [],
            "nearby_agents": []
        }
        
        # Find nearby resources
        for loc_name, loc_pos in self.state["world_state"]["locations"].items():
            distance = ((agent_pos["x"] - loc_pos["x"])**2 + 
                       (agent_pos["y"] - loc_pos["y"])**2)**0.5
            if distance < 5:  # Observation radius
                observations["nearby_resources"].append({
                    "name": loc_name,
                    "position": loc_pos,
                    "distance": distance
                })
        
        # Find nearby agents
        for other_id, other_agent in self.state["agents"].items():
            if other_id != agent_id:
                other_pos = other_agent["position"]
                distance = ((agent_pos["x"] - other_pos["x"])**2 + 
                           (agent_pos["y"] - other_pos["y"])**2)**0.5
                if distance < 5:  # Observation radius
                    observations["nearby_agents"].append({
                        "id": other_id,
                        "type": other_agent["type"],
                        "position": other_pos,
                        "distance": distance
                    })
        
        # Store observation in agent's knowledge
        if "observations" not in self.state["agents"][agent_id]["knowledge"]:
            self.state["agents"][agent_id]["knowledge"]["observations"] = []
        
        self.state["agents"][agent_id]["knowledge"]["observations"].append({
            "data": observations,
            "timestep": self.state["world_state"]["timestep"]
        })
        
        return {
            "success": True,
            "message": "Observation completed",
            "observations": observations
        }

    def _update_environment(self):
        """Update the environment state after each step."""
        # Increase timestep
        self.state["world_state"]["timestep"] += 1
        
        # Update agent statuses (detect inactive agents, etc.)
        for agent_id, agent in self.state["agents"].items():
            if agent["resources"]["energy"] <= 0:
                agent["status"] = "inactive"
            
        # Potentially replenish resources or add environmental events
        if self.state["world_state"]["timestep"] % 10 == 0:
            self.state["world_state"]["resources"]["energy"] += 5
            self.state["world_state"]["resources"]["materials"] += 3