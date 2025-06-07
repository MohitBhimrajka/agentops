from google.adk.agents import Agent

root_agent = Agent(
    name="agentops_echo",
    model="gemini-2.0-flash-001",
    instruction="You are an echo bot. Repeat exactly what the user says."
)
