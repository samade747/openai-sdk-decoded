import asyncio
from dotenv import load_dotenv
from agents import Agent, Runner, TResponseInputItem, enable_verbose_stdout_logging, AgentHook
from agents.run import AgentRunner, self_default_agent_runner
import rich

# ---------------------
load_dotenv()
enable_verbose_stdout_logging()
#  -----------
# custom class to change the result 

class MyCustomAgentRunClass(AgentRunner):
    async def run(self, starting_agent: Agent, input: str | list[TResponseInputItem], **kwargs) -> str:
        res = await super().run(starting_agent, input, **kwargs)
        res.final_output = "I'm samad and this is my custom response"
        

        return res
#  -----------
self_default_agent_runner(MyCustomAgentRunClass())    

#  -----------  

agent = Agent(
    name = "triage_agnet",
    instructions="yoi are a helpul assitant",
    model="gpt-4.1-mini",
    )

# ----------------------

async def main():
    result = await Runner.run(agent, input="hi")
    rich.print(result.final_output)

asyncio.run(main())