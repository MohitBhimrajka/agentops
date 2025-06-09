from google.adk.agents import Agent
from google.adk.tools import google_search

root_agent = Agent(
    name="basic_search_agent",
    model="gemini-2.0-flash",
    description="An agent that answers questions using Google Search.",
    instruction="Answer the user's questions using Google Search.",
    tools=[google_search]
)