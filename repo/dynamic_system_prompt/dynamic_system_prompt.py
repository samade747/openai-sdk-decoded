import asyncio
import random
from typing import Literal

# Import necessary components from the OpenAI Agents SDK
from agents import Agent, RunContextWrapper, Runner


# Step 1: Define a custom context to hold the style (haiku, pirate, or robot)
class CustomContext:
    def __init__(self, style: Literal["haiku", "pirate", "robot"]):
        self.style = style


# Step 2: Define a function to provide dynamic system instructions based on context
def custom_instructions(
    run_context: RunContextWrapper[CustomContext], agent: Agent[CustomContext]
) -> str:
    context = run_context.context
    if context.style == "haiku":
        return "Only respond in haikus."
    elif context.style == "pirate":
        return "Respond as a pirate."
    else:
        return "Respond as a robot and say 'beep boop' a lot."


# Step 3: Create an agent with a name and dynamic instruction handler
agent = Agent(
    name="Chat agent",
    instructions=custom_instructions,
)


# Step 4: Main async function to run the agent with random style context
async def main():
    # Randomly pick a style for the agent
    choice: Literal["haiku", "pirate", "robot"] = random.choice(["haiku", "pirate", "robot"])
    context = CustomContext(style=choice)

    print(f"Using style: {choice}\n")

    # The user's message
    user_message = "Tell me a joke."
    print(f"User: {user_message}")

    # Run the agent with the user's message and the dynamic context
    result = await Runner.run(agent, user_message, context=context)

    # Display the final response from the assistant
    print(f"Assistant: {result.final_output}")


# Step 5: Run the async main function
if __name__ == "__main__":
    asyncio.run(main())
