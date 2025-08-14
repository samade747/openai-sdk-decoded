import os 
from dotenv import load_dotenv
from agents import Agent, Runner, set_tracing_disabled, OpenAI
import rich

# ---------------------

 load_dotenv()

#  -----------

set_tracing_disabled(disabled=True)

#  -----------


OPENROUTER_API_KEY = os.getenv("OPENROUTER_API_KEY")


agent = Agent(
    name = "triage_agnet",
    instructions="yoi are a helpul assitant",
    model="gpt-4.1-mini",
)

# ----------------------

result = Runner.run_sync(agent, input="hi")
rich.print(result.final_output)""