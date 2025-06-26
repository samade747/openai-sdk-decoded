import asyncio
import random

from agents import Agent, ItemHelpers, Runner, function_tool

# 🎲 Tool to decide how many jokes to tell
@function_tool
def how_many_jokes() -> int:
    """Randomly pick a number between 1 and 10"""
    return random.randint(1, 10)

# 🚀 Main async function
async def main():
    # 🧠 Create agent with tool
    agent = Agent(
        name="Joker",
        instructions="First call the `how_many_jokes` tool, then tell that many jokes.",
        tools=[how_many_jokes],
    )

    # 🔁 Run the agent in streamed mode
    result = Runner.run_streamed(
        agent,
        input="Hello",  # 🔹 This will trigger the instruction above
    )

    print("=== Run starting ===")

    # 🧩 Process each event in the stream
    async for event in result.stream_events():
        # Skip raw delta events
        if event.type == "raw_response_event":
            continue

        # When agent is updated
        elif event.type == "agent_updated_stream_event":
            print(f"Agent updated: {event.new_agent.name}")
            continue

        # Handle run events (tool called, output, or message)
        elif event.type == "run_item_stream_event":
            if event.item.type == "tool_call_item":
                print("-- Tool was called")
            elif event.item.type == "tool_call_output_item":
                print(f"-- Tool output: {event.item.output}")
            elif event.item.type == "message_output_item":
                print(f"-- Message output:\n {ItemHelpers.text_message_output(event.item)}")
            else:
                pass  # Ignore other event types

    print("=== Run complete ===")

# 🔁 Entry point
if __name__ == "__main__":
    asyncio.run(main())
