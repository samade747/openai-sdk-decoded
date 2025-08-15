import os 
from dotenv import load_dotenv
from agents import Agent, Runner, set_tracing_disabled, OpenAIChatCompletionsModel, AsyncOpenAI, function_tool, WebSearchTool
import rich

# ---------------------
load_dotenv()
#  -----------
set_tracing_disabled(disabled=True)
#  -----------
OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")

if not OPENAI_API_KEY:
    raise ValueError("OPENAI_API_KEY not found in environment variables.")
#  -----------
client = AsyncOpenAI(
    base_url="https://api.openai.com/v1",
    api_key=OPENAI_API_KEY
)
#  -----------
@function_tool
async def looking_fortime(city: str) -> str:
    """
    Returns the current time information for a given U.S. city.
    """
    return f"Please search for the current time in {city}, USA."

#  -----------
agent = Agent(
    name = "triage_agnet",
    instructions="You are a helpful assistant that searches and provides answers from the internet.",
    model="gpt-4.1",
    tools=[WebSearchTool()],
    
   
)

# ----------------------

result = Runner.run_sync(agent, input="what is the time in usa washington? search on internet and give me the answer",)
rich.print(result.final_output)