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
    instructions=(
        "You are a triage agent, you delegate task to appropriate or use appropriate given tools"
        "when user asked for shopping related qurey, you always use given tools"
        "you never reply on your own, always use given tool to reply user"
        ),
    model="gpt-4.1-mini",
    openai_client=client,
    handoff_description="a support agent to help user in post-purchase queries",
    tools=[
        shopping_agent.as_tool(
            tool_name = "transfer_to_shopping_agent",
            tool_description = "you assist to finding products and making purchase decisions"
        ),
        support_agent.as_tool(
            tool_name = "transfer_to_support_agent",
            tool_description = "you assist user to finding products and making purchase decisions"
        )
    ]
)