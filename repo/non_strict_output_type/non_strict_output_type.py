import asyncio
import json
from dataclasses import dataclass
from typing import Any

from agents import Agent, AgentOutputSchema, AgentOutputSchemaBase, Runner

"""
This example demonstrates:
1. What happens when you use a non-strict JSON output schema.
2. How to enable non-strict mode.
3. How to build a fully custom output schema.
"""

# ✅ This output type expects a dictionary of jokes by number
@dataclass
class OutputType:
    jokes: dict[int, str]  # Example: {1: "Why did...", 2: "Knock knock..."}

# ✅ A custom output schema to parse non-standard or flexible output
class CustomOutputSchema(AgentOutputSchemaBase):
    def is_plain_text(self) -> bool:
        return False

    def name(self) -> str:
        return "CustomOutputSchema"

    def json_schema(self) -> dict[str, Any]:
        return {
            "type": "object",
            "properties": {
                "jokes": {
                    "type": "object",
                    "properties": {
                        "joke": {"type": "string"}
                    }
                }
            },
        }

    def is_strict_json_schema(self) -> bool:
        return False  # Important for allowing flexible JSON

    def validate_json(self, json_str: str) -> Any:
        json_obj = json.loads(json_str)
        # Convert object to list of jokes
        return list(json_obj["jokes"].values())

# ✅ Main execution logic
async def main():
    agent = Agent(
        name="Assistant",
        instructions="You are a helpful assistant.",
        output_type=OutputType,
    )

    input = "Tell me 3 short jokes."

    # 1️⃣ Try in strict mode – expected to fail
    try:
        result = await Runner.run(agent, input)
        raise AssertionError("Should have raised an exception")
    except Exception as e:
        print(f"Error (expected): {e}")

    # 2️⃣ Try again with strict_json_schema=False
    agent.output_type = AgentOutputSchema(OutputType, strict_json_schema=False)
    result = await Runner.run(agent, input)
    print("\nNon-strict Output:")
    print(result.final_output)

    # 3️⃣ Try with custom output schema
    agent.output_type = CustomOutputSchema()
    result = await Runner.run(agent, input)
    print("\nCustom Schema Output:")
    print(result.final_output)

if __name__ == "__main__":
    asyncio.run(main())
