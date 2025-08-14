import os 
from dotenv import load_dotenv
from agents import Agent, Runner, set_tracing_disabled, OpenAIChatCompletionsModel, AsyncOpenAI, function_tool
import rich

# ---------------------
load_dotenv()
#  -----------
set_tracing_disabled(disabled=True)
#  -----------
OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")

client = AsyncOpenAI(
    base_url="https://api.openai.com/v1",
    api_key= OPENAI_API_KEY
)

@function_tool
async def looking_fortime(query: str) -> str:
    """
    This function searches the internet for the current time in a specified location.
    """


    return f"the current time in {query} is 10:00 AM"  # Placeholder for actual implementation


agent = Agent(
    name = "triage_agnet",
    instructions="yoi are a helpul assitant",
    model=OpenAIChatCompletionsModel(model="gpt-4.1-mini", openai_client=client),
    tools=[looking_fortime],
   
)

# ----------------------

result = Runner.run_sync(agent, input="what is the time in usa washington? search on internet and give me the answer",)
rich.print(result.final_output)