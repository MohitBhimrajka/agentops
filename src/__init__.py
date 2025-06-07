from google.adk import load_agent_from_resource

# Load the root agent orchestrator from its YAML definition.
# The ADK will recursively load all child agents defined within it.
root_agent = load_agent_from_resource("src/agents/agentops_root.yaml")