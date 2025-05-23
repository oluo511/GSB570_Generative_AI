import os
import yaml

class AgentBase:
    def __init__(self, agent_id):
        # Get the directory of the current script
        current_dir = os.path.dirname(os.path.abspath(__file__))
        # Navigate up to the project root and then to the config directory
        project_root = os.path.dirname(os.path.dirname(current_dir))
        config_file = os.path.join(project_root, "config", "agents.yml")
        
        self.agent_id = agent_id
        self.config = self.load_config(config_file)
        self.agent_config = self.config.get(agent_id, {})
        
        print(f"Initialized {agent_id} agent with config: {self.agent_config}")
    
    def load_config(self, config_file):
        """Load configuration from a YAML file."""
        try:
            with open(config_file, "r") as file:
                config = yaml.safe_load(file)
                print(f"Successfully loaded config from {config_file}")
                return config
        except FileNotFoundError:
            print(f"Config file not found: {config_file}")
            print(f"Current working directory: {os.getcwd()}")
            raise
        except yaml.YAMLError as e:
            print(f"Error parsing YAML file: {e}")
            raise
    
    def process(self, data):
        """Process data according to the agent's logic."""
        # This should be overridden by derived classes
        raise NotImplementedError("Subclasses must implement this method")
    
    def run(self, input_data):
        """Run the agent on the provided input data."""
        result = self.process(input_data)
        return result

# Example usage
if __name__ == "__main__":
    try:
        agent = AgentBase("whitepaper_analyst")
        # Test with some dummy data
        result = agent.run({"text": "Sample whitepaper content"})
        print(f"Result: {result}")
    except Exception as e:
        print(f"Error: {e}")