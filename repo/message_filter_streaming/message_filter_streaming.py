from __future__ import annotations
import json
import random
import asyncio

# Import OpenAI Agents SDK core components
from agents import (
    Agent,
    HandoffInputData,
    Runner,
    function_tool,
    handoff,
    trace
)

# Import built-in filters for message history
from agents.extensions import handoff_filters


# 🔧 Tool Definition
@function_tool
def random_number_tool(max: int) -> int:
    """Returns a random number between 0 and max."""
    return random.randint(0, max)


# 🧹 Message Filter Function for Spanish Agent Handoff
def spanish_handoff_message_filter(handoff_message_data: HandoffInputData) -> HandoffInputData:
    # 1. Remove tool-related messages from the conversation history
    handoff_message_data = handoff_filters.remove_all_tools(handoff_message_data)

    # 2. Optionally remove the first 2 user messages from history (just for demonstration)
    history = (
        tuple(handoff_message_data.input_history[2:])
        if isinstance(handoff_message_data.input_history, tuple)
        else handoff_message_data.input_history
    )

    return HandoffInputData(
        input_history=history,
        pre_handoff_items=tuple(handoff_message_data.pre_handoff_items),
        new_items=tuple(handoff_message_data.new_items),
    )


# 🧠 First agent — Can generate a number using a tool
first_agent = Agent(
    name="Assistant",
    instructions="Be extremely concise.",
    tools=[random_number_tool],
)

# 🌐 Spanish-speaking agent
spanish_agent = Agent(
    name="Spanish Assistant",
    instructions="You only speak Spanish and are extremely concise.",
    handoff_description="A Spanish-speaking assistant.",
)

# 🧠 Second agent — Detects Spanish and hands off if needed
second_agent = Agent(
    name="Assistant",
    instructions="Be a helpful assistant. If the user speaks Spanish, handoff to the Spanish assistant.",
    handoffs=[
        handoff(
            spanish_agent,
            input_filter=spanish_handoff_message_filter  # message history cleaner before handoff
        )
    ],
)


# 🔁 Main logic using streaming output
async def main():
    with trace(workflow_name="Streaming message filter"):
        # Step 1: Greet the agent
        result = await Runner.run(first_agent, input="Hi, my name is Sora.")
        print("Step 1 done")

        # Step 2: Ask for a random number (tool will be called)
        result = await Runner.run(
            first_agent,
            input=result.to_input_list() + [
                {"content": "Can you generate a random number between 0 and 100?", "role": "user"}
            ],
        )
        print("Step 2 done")

        # Step 3: Ask a general knowledge question (in English)
        result = await Runner.run(
            second_agent,
            input=result.to_input_list() + [
                {"content": "I live in New York City. Whats the population of the city?", "role": "user"}
            ],
        )
        print("Step 3 done")

        # Step 4: Ask in Spanish — should cause handoff
        stream_result = Runner.run_streamed(
            second_agent,
            input=result.to_input_list() + [
                {
                    "content": "Por favor habla en español. ¿Cuál es mi nombre y dónde vivo?",
                    "role": "user",
                }
            ],
        )

        # Stream the response (you can print live tokens here if desired)
        async for _ in stream_result.stream_events():
            pass

        print("Step 4 done")

    # Step 5: Final review of the cleaned conversation history
    print("\n===Final messages===\n")
    for item in stream_result.to_input_list():
        print(json.dumps(item, indent=2))


# ▶️ Script entrypoint
if __name__ == "__main__":
    asyncio.run(main())


# ✅ What You Learned from This Code

# | Concept                    | Description                                                           |
# | -------------------------- | --------------------------------------------------------------------- |
# | `@function_tool`           | A tool callable by the agent to generate a number                     |
# | `handoff()`                | Routes to another agent based on conditions (like language detection) |
# | `input_filter`             | Filters or trims the history sent to the new agent                    |
# | `Runner.run_streamed()`    | Streams the agent's output token-by-token                             |
# | `trace(workflow_name=...)` | Traces the full agent session for better debugging                    |
