import asyncio
from agents import Agent, Runner

"""
Demonstrates how to maintain conversation history using `previous_response_id`.
This works ONLY with OpenAI Responses API.
"""

async def main():
    agent = Agent(
        name="Assistant",
        instructions="You are a helpful assistant. Be VERY concise.",
    )

    # First user input
    result = await Runner.run(agent, "What is the largest country in South America?")
    print(result.final_output)

    # Second input, continue conversation
    result = await Runner.run(
        agent,
        "What is the capital of that country?",
        previous_response_id=result.last_response_id,
    )
    print(result.final_output)

async def main_stream():
    agent = Agent(
        name="Assistant",
        instructions="You are a helpful assistant. Be VERY concise.",
    )

    # First question streamed
    result = Runner.run_streamed(agent, "What is the largest country in South America?")
    async for event in result.stream_events():
        if event.type == "raw_response_event" and event.data.type == "response.output_text.delta":
            print(event.data.delta, end="", flush=True)
    print()

    # Second question with previous response ID
    result = Runner.run_streamed(
        agent,
        "What is the capital of that country?",
        previous_response_id=result.last_response_id,
    )
    async for event in result.stream_events():
        if event.type == "raw_response_event" and event.data.type == "response.output_text.delta":
            print(event.data.delta, end="", flush=True)

if __name__ == "__main__":
    is_stream = input("Run in stream mode? (y/n): ")
    if is_stream == "y":
        asyncio.run(main_stream())
    else:
        asyncio.run(main())



📌 Notes
This feature only works with OpenAI’s Responses API.

previous_response_id lets the model continue the chat from the last known response.

Response IDs are valid for 30 days, so store them if using in production.

🧠 Use Cases
Memory-like follow-ups without needing full chat history

Stateless APIs with minimal token cost

High-performance, contextual Q&A apps