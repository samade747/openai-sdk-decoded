# This example uses the OpenAI Python Agents SDK to build a triage agent system with:

# A guardrail to filter whether the input is a homework question

# Two specialist agents (history and math)

# A triage agent that decides who to handoff to


import asyncio
import os
from dotenv import load_dotenv, find_dotenv
from agents import Agent, Runner, OpenAIChatCompletionsModel, AsyncOpenAI, GuardrailFunctionOutput, InputGuardrail, function_tool
from pydantic import BaseModel
# asyncio: Run async code (used for async agent operations).
# dotenv: Loads .env file to get environment variables like API keys.
# agents: OpenAI Agents SDK.
# pydantic: For defining structured output formats.


# Define Output Schema with Pydantic
class HomeworkOutput(BaseModel):
    is_homework: bool
    reasoning: str
# This tells the Guardrail Agent to return:
# Whether the question is homework (True/False)
# A string explanation (reasoning)

load_dotenv(find_dotenv())
provider = AsyncOpenAI(base_url="https://api.openai.com/v1",
                       api_key=os.getenv("OPENAI_API_KEY"))

# Define a Dummy Tool
@function_tool
def get_weather(city: str) -> str:
    return f"The weather in {city} is sunny"
# This is an example function_tool, not used in this code run, but shows how tools are defined.


# define agent
history_agent = Agent(
    name="history_agent",
    handoff_description="specializes in history questions",
    instructions="You provide assistance with historical queries. Explain important events and context clearly.",
)

math_tutor_agent = Agent(
    name="Math Tutor",
    handoff_description="Specialist agent for math questions",
    instructions="You provide help with math problems. Explain your reasoning at each step and include examples",
)
# Each agent:
# Has a name and description (used by parent agents to decide handoff)
# Has specific instructions

#  Guardrail Agent Definition 
guardrail_agent = Agent(
    name="Guardrail check",
    instructions="check if the user is asking about homework",
    output_type=HomeworkOutput,
)

# This agent:
# Receives user input
# Returns is_homework=True/False and a reason using the HomeworkOutput schema

#  Guardrail Logic Function
async def homework_guardrail(ctx, agent: Agent, input_data):
    print("Received Agnet in GD", agent.name)
    reuslt = await Runner.run(guardrail_agent, input_data, context=ctx.context)
    print("Guardrail result:", reuslt)
    final_output = reuslt.final_output_as(HomeworkOutput)
    print("Final output from guardrail:", final_output)
    return GuardrailFunctionOutput(
        output_info=final_output,
        tripwire_triggered=not final_output.is_homework
    )

# main logic 
async def main():
    #Create the triage agnet
    agent = Agent(
        name="Triage Agent",
        intsrtuctions = "You determine which agent to use based on the user's homework question",
        handoffs=[history_agent, math_tutor_agent],
        input_guardrails=[InputGuardrail(homework_guardrail)],
    )

    # Run the agent with a sample qurey
    result = await Runner.run(agent, "I have homework about the french revolution. Can you help me?")
    print(result.final_output)

# Run the main function
if __name__ == "__main__":
    print("\n[STARTING AGENT]\n")
    asyncio.run(main())