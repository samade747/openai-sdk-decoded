# from dotenv import load_dotenv
# from agents import Agent, Runner, input_guardrail, GuardrailFunctionOutput, RunContextWrapper, TResponseInputItem
# import rich

# load_dotenv()

# # ------ INPUT GUARDRAIL DECORATOR
# # ---- creating decorator for input guardrail

# @input_guardrail
# def psx_position_check(ctx: RunContextWrapper, agent: Agent, input: str | list[TResponseInputItem]) -> GuardrailFunctionOutput:
    
#     return GuardrailFunctionOutput(
#         output_info="",
#         tripwire_triggered=""
#     )


# # ------CREATING AGENT WITH 
# agent = Agent(
#     name = "triage_agent",
#     instructions="you are a helpful assistant",
#     model="gpt-4o",
#     input_guardrails=[]
# )


# # ----- 

# result = Runner.run_sync(agent, input="hi")
# rich.print(result.final_output)
