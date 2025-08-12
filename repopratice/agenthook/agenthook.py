from dotenv import load_dotenv
from agents import Agent, Runner, AsyncOpenAI, OpenAIChatCompletionsModel, RunConfig
import rich


# ---------------------

load_dotenv()

#  -----------

agent = Agent(
    name = "triage_agnet",
    instructions="yoi are a helpul assitant",
    model="gpt-4o",
)

# ----------------------

agent.run("what is the meaning of life")