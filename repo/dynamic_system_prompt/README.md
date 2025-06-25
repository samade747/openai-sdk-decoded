import asyncio
import random
from typing import Literal

# Import Agent components from OpenAI Agents SDK
from agents import Agent, RunContextWrapper, Runner


# Custom context class that holds the style of response
class CustomContext:
    def __init__(self, style: Literal["haiku", "pirate", "robot"]):
        self.style = style


# Dynamic instruction generator based on the context
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


# Create the agent with the dynamic instructions
agent = Agent(
    name="Chat agent",
    instructions=custom_instructions,
)


# Main function to run the agent
async def main():
    # Randomly select a style
    choice: Literal["haiku", "pirate", "robot"] = random.choice(["haiku", "pirate", "robot"])
    context = CustomContext(style=choice)

    print(f"Using style: {choice}\n")

    # Static user input
    user_message = "Tell me a joke."
    print(f"User: {user_message}")

    # Run the agent with the selected context
    result = await Runner.run(agent, user_message, context=context)

    # Output the result
    print(f"Assistant: {result.final_output}")


# Entry point
if __name__ == "__main__":
    asyncio.run(main())
