import os
from dotenv import load_dotenv
from agents import Agent, Runner, AsyncOpenAI

# # ---------------------

load_dotenv()


OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")

if not OPENAI_API_KEY:
    raise ValueError("OPENAI_API_KEY not found in environment variables.")

# # ---------------------

client = AsyncOpenAI(
    base_url="https://api.openai.com/v1",
    api_key=os.getenv("OPENAI_API_KEY")
)

# # ---------------------
shopping_agent = Agent(
    name="shopping_agent",
    instructions="you help user with post-purchase support",
    handoff_description="You are a helpful assistant that helps users with post-purchase support.",
)
# # ---------------------

support_agent = Agent(
    name="shopping_agent",
    instructions="you assist user to finding products and making purchase decisions",
    handoff_description="You are a helpful assistant that helps users find products and make purchase decisions.",
    
)   

# # ---------------------
triage_agent = Agent(
    name="triage_agent",
    instructions=("You are a helpful assistant that triages requests"),
    model="gpt-4.1-mini",
    openai_client=client,
    # handoff_description=("You are a helpful assistant that triages requests and hands off to the appropriate agent."),
    tools=[
        shopping_agent.as_tool()
    ]
)