import asyncio
import os
from dotenv import load_dotenv
from pydantic import BaseModel
from agents import (
    Agent,
    OpenAIChatCompletionsModel,
    Runner,
    RunConfig,
    RunContextWrapper,
    function_tool,
    input_guardrail,
    output_guardrail,
    GuardrailFunctionOutput,
    TResponseInputItem
)
from openai import AsyncOpenAI

# Load environment
load_dotenv()
openai_api_key = os.getenv("OPENAI_API_KEY")
if not openai_api_key:
    raise ValueError("OPENAI_API_KEY not found in environment variables.")

# Initialize OpenAI client and model
client = AsyncOpenAI(api_key=openai_api_key)
model = OpenAIChatCompletionsModel(model="gpt-4o-mini", openai_client=client)
config = RunConfig(model=model, tracing_disabled=True, model_provider=client)

# Context schema
class user_info(BaseModel):
    name: str
    is_premium: bool
    issue_type: str  # 'technical', 'billing', 'refund'

# Tools
def _refund_logic(ctx: RunContextWrapper[user_info]) -> str:
    if ctx.context.is_premium:
        return f"Refund processed successfully for {ctx.context.name}."
    return f"{ctx.context.name}, you need a premium subscription to request a refund."

@function_tool(
    is_enabled=lambda ctx, agent: ctx.context.issue_type == "refund"
)
def refund(ctx: RunContextWrapper[user_info]) -> str:
    """Process a refund only if the user is premium."""
    return _refund_logic(ctx)

@function_tool(
    is_enabled=lambda ctx, agent: not ctx.context.is_premium
)
def check_issue_type(ctx: RunContextWrapper[user_info]) -> str:
    """Return issue type to help route non-premium users."""
    return ctx.context.issue_type

@function_tool(
    is_enabled=lambda ctx, agent: ctx.context.issue_type == "technical"
)
def restart_service(ctx: RunContextWrapper[user_info]) -> str:
    """Restart the user's service (technical support)."""
    return f"Technical service has been restarted for {ctx.context.name}."

# Input guardrail
class SupportIntentOutput(BaseModel):
    is_support_related: bool
    reasoning: str

support_guardrail_agent = Agent(
    name="SupportIntentChecker",
    instructions=(
        "Determine if the user is asking a customer support issue (billing, refund, technical)."
        "Return is_support_related=True/False and reasoning."
    ),
    output_type=SupportIntentOutput,
    model=model
)

@input_guardrail
async def support_input_guardrail(ctx, agent, input: str | list[TResponseInputItem]) -> GuardrailFunctionOutput:
    result = await Runner.run(support_guardrail_agent, input, context=ctx.context)
    return GuardrailFunctionOutput(
        output_info=result.final_output,
        tripwire_triggered=not result.final_output.is_support_related
    )

# Output guardrail
class CleanSupportResponse(BaseModel):
    contains_blocked_phrase: bool
    reason: str

blocklist_output_agent = Agent(
    name="BlockedPhraseChecker",
    instructions=(
        "Check if output contains 'I'm sorry', 'as an AI', 'LLM', 'I cannot'."
        "Set contains_blocked_phrase=True/False and reason."
    ),
    output_type=CleanSupportResponse,
    model=model
)

@output_guardrail
async def support_output_guardrail(ctx, agent, output: str) -> GuardrailFunctionOutput:
    result = await Runner.run(blocklist_output_agent, output, context=ctx.context)
    return GuardrailFunctionOutput(
        output_info=result.final_output,
        tripwire_triggered=result.final_output.contains_blocked_phrase
    )

# Main
async def main():
    # Define specialized agents
    tech_agent = Agent(
        name="tech_agent",
        instructions="Handle technical issues.",
        tools=[restart_service]
    )
    billing_agent = Agent(
        name="billing_agent",
        instructions="Handle billing issues."
    )
    refund_agent = Agent(
        name="refund_agent",
        instructions="Handle refund requests.",
        tools=[refund]
    )
    
    # Triage agent
    support_agent = Agent(
        name="support_agent",
        instructions="""
        Delegate to technical_agent, billing_agent, or refund_agent based on context.issue_type.
        Never respond directly; always handoff.
        """,
        handoffs=[tech_agent, billing_agent, refund_agent],
        handoff_description="Use context.issue_type to choose agent.",
        tools=[check_issue_type],
        input_guardrails=[support_input_guardrail],
        output_guardrails=[support_output_guardrail]
    )

    print("📞 Console Support Agent System Started! (type 'exit' to quit)")
    while True:
        user_input = input("💬 User Input: ")
        if user_input.lower() in ["exit", "quit"]:
            print("👋 Goodbye!")
            break

        issue_type = input("🔧 Issue type (technical/billing/refund): ").strip().lower()
        is_premium = input("💎 Premium user? (yes/no): ").strip().lower() in ["yes", "y"]
        context = user_info(name="samad", is_premium=is_premium, issue_type=issue_type)

        print("\n🤖 Agent response:")
        result = await Runner.run(
            support_agent,
            input=user_input,
            context=context,
            run_config=config
        )

        # Print the final output
        if result.final_output is not None:
            print(f"\n✅ Final Output: {result.final_output}")
        else:
            print("\n❌ No final output (possibly tripped by guardrails)")
        print("\n" + "-"*50 + "\n")

if __name__ == "__main__":
    asyncio.run(main())
