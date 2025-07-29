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