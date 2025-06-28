import asyncio
from openai.types.responses import ResponseTextDeltaEvent
from agents import Agent, Runner

# Main async function
async def main():
    # Step 1: Create an agent with basic instructions
    agent = Agent(
        name="Joker",
        instructions="You are a helpful assistant.",
    )

    # Step 2: Start a streaming run of the agent with user input
    result = Runner.run_streamed(agent, input="Please tell me 5 jokes.")

    # Step 3: As response is being generated, handle it piece by piece
    async for event in result.stream_events():
        # Only handle text response chunks
        if event.type == "raw_response_event" and isinstance(event.data, ResponseTextDeltaEvent):
            print(event.data.delta, end="", flush=True)  # Print each token/word live

# Run the code
if __name__ == "__main__":
    asyncio.run(main())
