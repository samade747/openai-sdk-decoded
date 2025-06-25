import argparse
import asyncio
import random

from agents import Agent, GenerateDynamicPromptData, Runner

"""
Demonstrates use of static and dynamic prompt injection using OpenAI prompt templates.

You must create a prompt on:
https://platform.openai.com/playground/prompts
"""

# Placeholder default (won't work unless it's your own prompt)
DEFAULT_PROMPT_ID = "pmpt_6850729e8ba481939fd439e058c69ee004afaa19c520b78b"

# 🔁 Dynamic context class to randomly choose a poem style
class DynamicContext:
    def __init__(self, prompt_id: str):
        self.prompt_id = prompt_id
        self.poem_style = random.choice(["limerick", "haiku", "ballad"])
        print(f"[debug] DynamicContext initialized with poem_style: {self.poem_style}")

# 🧠 Dynamic prompt injector
async def _get_dynamic_prompt(data: GenerateDynamicPromptData):
    ctx: DynamicContext = data.context.context
    return {
        "id": ctx.prompt_id,
        "version": "1",
        "variables": {
            "poem_style": ctx.poem_style,
        },
    }

# 🧪 Agent using dynamic prompt
async def dynamic_prompt(prompt_id: str):
    context = DynamicContext(prompt_id)

    agent = Agent(
        name="Assistant",
        prompt=_get_dynamic_prompt,  # async function for dynamic prompt
    )

    result = await Runner.run(
        agent,
        "Tell me about recursion in programming.",
        context=context,
    )

    print(result.final_output)

# 🔒 Agent using static prompt
async def static_prompt(prompt_id: str):
    agent = Agent(
        name="Assistant",
        prompt={
            "id": prompt_id,
            "version": "1",
            "variables": {
                "poem_style": "limerick",
            },
        },
    )

    result = await Runner.run(agent, "Tell me about recursion in programming.")
    print(result.final_output)

# 🏁 CLI entrypoint
if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("--dynamic", action="store_true")
    parser.add_argument("--prompt-id", type=str, default=DEFAULT_PROMPT_ID)
    args = parser.parse_args()

    if args.dynamic:
        asyncio.run(dynamic_prompt(args.prompt_id))
    else:
        asyncio.run(static_prompt(args.prompt_id))
