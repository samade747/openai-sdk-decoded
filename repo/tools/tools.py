import asyncio
from pydantic import BaseModel
from agents import Agent, Runner, function_tool

# Step 1: Define the structure for weather data
class Weather(BaseModel):
    city: str
    temperature_range: str
    conditions: str

# Step 2: Create a tool that provides weather data
@function_tool
def get_weather(city: str) -> Weather:
    print("[debug] get_weather called")  # Debug message to show tool was triggered
    return Weather(
        city=city,
        temperature_range="14-20C",
        conditions="Sunny with wind."
    )

# Step 3: Create the agent and register the tool
agent = Agent(
    name="Hello world",
    instructions="You are a helpful agent.",
    tools=[get_weather],  # Register our custom tool
)

# Step 4: Main async function to run the agent with user input
async def main():
    result = await Runner.run(agent, input="What's the weather in Tokyo?")
    print(result.final_output)  # Print the agent's final reply

# Step 5: Run the async main
if __name__ == "__main__":
    asyncio.run(main())
