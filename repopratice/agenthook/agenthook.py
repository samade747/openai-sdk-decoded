from dotenv import load_dotenv
from agents import Agent, Runner, AgentHooks
import rich


# ---------------------

load_dotenv()

#  -----------

class MyAgentHook(AgentHooks):
    pass

#  -----------

agent = Agent(
    name = "triage_agnet",
    instructions="yoi are a helpul assitant",
    model="gpt-4.1-mini",
)

# ----------------------

result = Runner.run_sync(agent, input="hi", hooks=MyAgentHook())
rich.print(result.final_output)