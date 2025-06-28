from __future__ import annotations
import json
import random
import asyncio

# Import necessary components from the OpenAI Agents SDK
from agents import (
    Agent,
    HandoffInputData,
    Runner,
    function_tool,
    handoff,
    trace,
)
from agents.extensions import handoff_filters


# 🎯 TOOL DEFINITION
@function_tool
def random_number_tool(max: int) -> int:
    """Return a random integer between 0 and the given maximum."""
    return random.randint(0, max)


# 🧼 FILTER FUNCTION: Cleans messages before handoff
def spanish_handoff_message_filter(handoff_message_data: HandoffInputData) -> HandoffInputData:
    # Step 1: Remove all tool-related messages from the conversation history
    handoff_message_data = handoff_filters.remove_all_tools(handoff_message_data)

    # Step 2: Remove the first two items from history (just for demonstration)
    history = (
        tuple(handoff_message_data.input_history[2:])
        if isinstance(handoff_message_data.input_history, tuple)
        else handoff_message_data.input_history
    )

    # Return the cleaned handoff input data
    return HandoffInputData(
        input_history=history,
        pre_handoff_items=tuple(handoff_message_data.pre_handoff_items),
        new_items=tuple(handoff_message_data.new_items),
    )


# 🤖 FIRST AGENT: Basic assistant with a random number tool
first_agent = Agent(
    name="Assistant",
    instructions="Be extremely concise.",
    tools=[random_number_tool],
)

# 🤖 SPANISH AGENT: Speaks only Spanish
spanish_agent = Agent(
    name="Spanish Assistant",
    instructions="You only speak Spanish and are extremely concise.",
    handoff_description="A Spanish-speaking assistant.",
)

# 🤖 SECOND AGENT: Hands off to Spanish agent if user speaks Spanish
second_agent = Agent(
    name="Assistant",
    instructions="Be a helpful assistant. If the user speaks Spanish, handoff to the Spanish assistant.",
    handoffs=[handoff(spanish_agent, input_filter=spanish_handoff_message_filter)],
)


# 🚀 MAIN WORKFLOW
async def main():
    # Wrap the entire run in a trace context for observability
    with trace(workflow_name="Message filtering"):
        # 🔹 STEP 1: Say hello
        result = await Runner.run(first_agent, input="Hi, my name is Sora.")
        print("Step 1 done")

        # 🔹 STEP 2: Generate a random number using the tool
        result = await Runner.run(
            first_agent,
            input=result.to_input_list() + [
                {"content": "Can you generate a random number between 0 and 100?", "role": "user"}
            ],
        )
        print("Step 2 done")

        # 🔹 STEP 3: Ask a normal question in English (handled by second_agent)
        result = await Runner.run(
            second_agent,
            input=result.to_input_list() + [
                {"content": "I live in New York City. Whats the population of the city?", "role": "user"}
            ],
        )
        print("Step 3 done")

        # 🔹 STEP 4: Ask in Spanish → triggers a handoff to spanish_agent
        result = await Runner.run(
            second_agent,
            input=result.to_input_list() + [
                {"content": "Por favor habla en español. ¿Cuál es mi nombre y dónde vivo?", "role": "user"}
            ],
        )
        print("Step 4 done")

    # ✅ PRINT FINAL CLEANED MESSAGES
    print("\n===Final messages===\n")
    for message in result.to_input_list():
        print(json.dumps(message, indent=2))


# 🔧 RUN THE APP
if __name__ == "__main__":
    asyncio.run(main())
