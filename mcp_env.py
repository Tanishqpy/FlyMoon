class MCPEnvironment:
    def __init__(self):
        self.state = "start"  # or state space like int, tuple, etc.

    def step(self, action):
        # Apply the transition logic based on current state and action
        # Example:
        if self.state == "start" and action == "move":
            self.state = "next"
        return {"state": self.state, "done": False, "info": "example"}

    def reset(self):
        self.state = "start"
        return {"state": self.state}
