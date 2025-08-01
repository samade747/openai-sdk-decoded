import asyncio
import random

from agents import Agent, ItemHelpers, Runner, function_tool

@function_tool
def how_many_jokes() -> int:
    return random.randint(1, 10)

async def main():
    agent = Agent(
        name="Joker",
        instructions="First call the `how_many_jokes` tool, then tell that many jokes.",
        tools=[how_many_jokes],
    )

    result = Runner.run_streamed(agent, input="Hello")

    print("=== Run starting ===")

    async for event in result.stream_events():
        if event.type == "raw_response_event":
            continue
        elif event.type == "agent_updated_stream_event":
            print(f"Agent updated: {event.new_agent.name}")
        elif event.type == "run_item_stream_event":
            if event.item.type == "tool_call_item":
                print("-- Tool was called")
            elif event.item.type == "tool_call_output_item":
                print(f"-- Tool output: {event.item.output}")
            elif event.item.type == "message_output_item":
                print(f"-- Message output:\n {ItemHelpers.text_message_output(event.item)}")

    print("=== Run complete ===")

if __name__ == "__main__":
    asyncio.run(main())


=== Run starting ===
Agent updated: Joker
-- Tool was called
-- Tool output: 4
-- Message output:
 Sure, here are four jokes for you:

1. Why don't skeletons fight each other?  
   They don't have the guts!

2. What do you call fake spaghetti?  
   An impasta!

3. Why did the scarecrow win an award?  
   Because he was outstanding in his field!

4. Why did the bicycle fall over?  
   Because it was two-tired!
=== Run complete ===
