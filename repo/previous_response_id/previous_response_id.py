import asyncio
from agents import Agent, Runner

"""
Demonstrates how to maintain conversation history using `previous_response_id`.

This works ONLY with OpenAI Responses API.

💡 Good for follow-up questions where you don’t want to resend the full message history.
"""

# ✅ Non-streamed conversation with context
async def main():
    # Create the agent with concise instruction
    agent = Agent(
        name="Assistant",
        instructions="You are a helpful assistant. Be VERY concise.",
    )

    # First question
    result = await Runner.run(agent, "What is the largest country in South America?")
    print(result.final_output)  # ➜ Brazil (expected)

    # Second question, passing previous_response_id to maintain context
    result = await Runner.run(
        agent,
        "What is the capital of that country?",
        previous_response_id=result.last_response_id,
    )
    print(result.final_output)  # ➜ Brasília (expected)

# ✅ Streamed version of the same logic
async def main_stream():
    agent = Agent(
        name="Assistant",
        instructions="You are a helpful assistant. Be VERY concise.",
    )

    # First streamed message
    result = Runner.run_streamed(agent, "What is the largest country in South America?")
    async for event in result.stream_events():
        if event.type == "raw_response_event" and event.data.type == "response.output_text.delta":
            print(event.data.delta, end="", flush=True)
    print()

    # Second message, continuing from the first
    result = Runner.run_streamed(
        agent,
        "What is the capital of that country?",
        previous_response_id=result.last_response_id,
    )
    async for event in result.stream_events():
        if event.type == "raw_response_event" and event.data.type == "response.output_text.delta":
            print(event.data.delta, end="", flush=True)

# ✅ Run the async function based on user input
if __name__ == "__main__":
    is_stream = input("Run in stream mode? (y/n): ")
    if is_stream == "y":
        asyncio.run(main_stream())
    else:
        asyncio.run(main())
