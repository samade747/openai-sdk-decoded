import asyncio
import json
from dataclasses import dataclass
from typing import Any

from agents import Agent, AgentOutputSchema, AgentOutputSchemaBase, Runner

# Define a dataclass output that is not JSON strict-compatible
@dataclass
class OutputType:
    jokes: dict[int, str]  # Example: {1: "Why did...", 2: "Knock knock..."}

# Define a custom output schema for non-strict or flexible JSON formats
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
        return False  # Disable strict JSON enforcement

    def validate_json(self, json_str: str) -> Any:
        json_obj = json.loads(json_str)
        return list(json_obj["jokes"].values())  # Flatten to list of jokes

# Main execution logic
async def main():
    agent = Agent(
        name="Assistant",
        instructions="You are a helpful assistant.",
        output_type=OutputType,
    )

    input = "Tell me 3 short jokes."

    # 1. Try with strict mode (this will fail)
    try:
        result = await Runner.run(agent, input)
        raise AssertionError("Should have raised an exception")
    except Exception as e:
        print(f"Error (expected): {e}")

    # 2. Try with non-strict JSON schema (may succeed)
    agent.output_type = AgentOutputSchema(OutputType, strict_json_schema=False)
    result = await Runner.run(agent, input)
    print("\nNon-strict Output:")
    print(result.final_output)

    # 3. Try with custom schema
    agent.output_type = CustomOutputSchema()
    result = await Runner.run(agent, input)
    print("\nCustom Schema Output:")
    print(result.final_output)

if __name__ == "__main__":
    asyncio.run(main())



    Error (expected): Failed to parse output with strict schema...

Non-strict Output:
{1: "Why don't skeletons fight each other?", 2: "They don't have the guts.", 3: "I'm afraid for the calendar. Its days are numbered."}

Custom Schema Output:
["Why don't skeletons fight each other?", "They don't have the guts.", "Its days are numbered."]

