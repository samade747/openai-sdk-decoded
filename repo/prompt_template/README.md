# ✨ OpenAI Agent – Static & Dynamic Prompt Injection Example

This project demonstrates how to use **prompt templates** with the [OpenAI Python Agents SDK](https://github.com/openai/openai-agents-python), including both **static** and **dynamic** prompt variable injection.

---

## 🧠 What This Project Shows

✅ Inject values into OpenAI **prompt templates**  
✅ Use **dynamic context** to generate variable values at runtime  
✅ Use **async function** to generate prompt data dynamically  
✅ Command-line flag to toggle between static/dynamic prompts

---

## 📦 Requirements

- Python 3.8+
- OpenAI Python Agents SDK
- A prompt template created in OpenAI Playground

---

## 🔧 Setup a Prompt Template

### 🪄 Steps:

1. Go to: [https://platform.openai.com/playground/prompts](https://platform.openai.com/playground/prompts)
2. Create a new prompt template with content:


3. Save it and copy the Prompt ID (e.g. `pmpt_abc123...`)

---

## ▶️ How to Run

### 🔁 Dynamic Mode (random style each time)

```bash
python dynamic_prompt_example.py --dynamic --prompt-id YOUR_PROMPT_ID


python dynamic_prompt_example.py --prompt-id YOUR_PROMPT_ID


import argparse
import asyncio
import random

from agents import Agent, GenerateDynamicPromptData, Runner

DEFAULT_PROMPT_ID = "pmpt_6850729e8ba481939fd439e058c69ee004afaa19c520b78b"

class DynamicContext:
    def __init__(self, prompt_id: str):
        self.prompt_id = prompt_id
        self.poem_style = random.choice(["limerick", "haiku", "ballad"])
        print(f"[debug] DynamicContext initialized with poem_style: {self.poem_style}")

async def _get_dynamic_prompt(data: GenerateDynamicPromptData):
    ctx: DynamicContext = data.context.context
    return {
        "id": ctx.prompt_id,
        "version": "1",
        "variables": {
            "poem_style": ctx.poem_style,
        },
    }

async def dynamic_prompt(prompt_id: str):
    context = DynamicContext(prompt_id)
    agent = Agent(name="Assistant", prompt=_get_dynamic_prompt)
    result = await Runner.run(agent, "Tell me about recursion in programming.", context=context)
    print(result.final_output)

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

if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("--dynamic", action="store_true")
    parser.add_argument("--prompt-id", type=str, default=DEFAULT_PROMPT_ID)
    args = parser.parse_args()

    if args.dynamic:
        asyncio.run(dynamic_prompt(args.prompt_id))
    else:
        asyncio.run(static_prompt(args.prompt_id))


$ python dynamic_prompt_example.py --dynamic --prompt-id pmpt_abcd1234...4

[debug] DynamicContext initialized with poem_style: ballad

In recursion's grasp so deep,
Where base case sings you to sleep,
The function calls again, again,
A cycle wrapped in code’s domain.


🧠 Real-World Use Cases
Multi-language prompt variables (poem_style, mood, tone)

Personalized user interactions

Dynamic chatbot personalities