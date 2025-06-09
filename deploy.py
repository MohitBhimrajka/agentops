import vertexai
from vertexai import agent_engines
from agent.agent import root_agent

vertexai.init(
    project="agentops-dev",
    location="us-central1",
    staging_bucket="gs://mohit-adk"
)

remote_app = agent_engines.create(
    agent_engine=root_agent,
    requirements=["google-cloud-aiplatform[agent_engines,adk]"],
    display_name="My ADK Agent",
    description="Agent deployed for custom frontend usage.",
)

print("Deployed:", remote_app.resource_name)
