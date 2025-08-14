import os 
from dotenv import load_dotenv
from agents import Agent, Runner, set_tracing_disabled

# # ---------------------

 load_dotenv()

# #  -----------

set_tracing



# class MyAgentHook(AgentHooks):
#     pass

# #  -----------

# agent = Agent(
#     name = "triage_agnet",
#     instructions="yoi are a helpul assitant",
#     model="gpt-4.1-mini",
# )

# # ----------------------

# result = Runner.run_sync(agent, input="hi", hooks=MyAgentHook())
# rich.print(result.final_output)