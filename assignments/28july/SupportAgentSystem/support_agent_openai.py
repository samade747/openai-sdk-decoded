# support_agent_openai.py

from agents import (
    Agent,
    OpenAIChatCompletionsModel,
    Runner,
    function_tool,
    RunConfig,
    RunContextWrapper,
    input_guardrail,
    output_guardrail,
    GuardrailFunctionOutput,
)
from openai import AsyncOpenAI
from dotenv import load_dotenv
from pydantic import BaseModel
import os
import asyncio

# ================= Load API Key ======================
load_dotenv()
openai_api_key = os.getenv("OPENAI_API_KEY")

if not openai_api_key:
    raise ValueError("OPENAI_API_KEY not found in environment variables.")

client = AsyncOpenAI(api_key=openai_api_key)

model = OpenAIChatCompletionsModel(
    model="gpt-4o",  # Or "gpt-3.5-turbo"
    openai_client=client
)

config = RunConfig(
    model=model,
    tracing_disabled=True,
    model_provider=client
)

# ================= Pydantic Context =====================
class user_info(BaseModel):
    name: str
    is_premium: bool
    issue_type: str  # 'technical', 'billing', 'refund'

# ================= Tools ================================

@function_tool(
    is_enabled=lambda ctx: ctx.context.issue_type == "refund"
)
def refund(ctx: RunContextWrapper[user_info]) -> str:
    if ctx.context.is_premium:
        return f"Refund processed successfully for {ctx.context.name}."
    return f"{ctx.context.name}, you need a premium subscription to request a refund."

@function_tool(
    is_enabled=lambda ctx: not ctx.context.is_premium
)
def check_issue_type(ctx: RunContextWrapper[user_info]) -> str:
    return ctx.context.issue_type

@function_tool(
    is_enabled=lambda ctx: ctx.context.issue_type == "technical"
)
def restart_service(ctx: RunContextWrapper[user_info]) -> str:
    return f"Technical service has been restarted for {ctx.context.name}."

# ================= Guardrails ============================
@input_guardrail
def validate_input(user_input: str) -> GuardrailFunctionOutput:
    blocked_phrases = ["abuse", "nonsense", "idiot", "shut up"]
    if any(bad_word in user_input.lower() for bad_word in blocked_phrases):
        return GuardrailFunctionOutput(valid=False, error="Inappropriate language is not allowed.")
    return GuardrailFunctionOutput(valid=True)

@output_guardrail
def restrict_apologies(output: str) -> GuardrailFunctionOutput:
    forbidden_phrases = ["sorry", "apologize", "unfortunately"]
    if any(phrase in output.lower() for phrase in forbidden_phrases):
        return GuardrailFunctionOutput(valid=False, error="No apology phrases allowed in output.")
    return GuardrailFunctionOutput(valid=True)

# ================= Main CLI App ============================
async def main():
    # ---- Sub-agents ----
    technical_agent = Agent(
        name="technical_agent",
        instructions="You handle technical issues like restarting services, bugs, or errors.",
        tools=[restart_service]
    )

    billing_agent = Agent(
        name="billing_agent",
        instructions="You handle billing questions including payments and charges."
    )

    refund_agent = Agent(
        name="refund_agent",
        instructions="You handle refund-related queries. Only serve premium users.",
        tools=[refund]
    )

    # ---- Main triage agent ----
    support_agent = Agent(
        name="customer_support_agent",
        instructions="""
        You are a helpful and polite customer service agent.
        Delegate issues to the appropriate agent and use tools when needed.
        Never respond directly to refund or technical or billing queries.
        Always rely on context and tools.
        """,
        handoffs=[technical_agent, billing_agent, refund_agent],
        handoff_description="Decide handoff based on context.issue_type.",
        tools=[check_issue_type],
        input_guardrails=[validate_input],
        output_guardrails=[restrict_apologies],
    )

    print("\n📞 Console Support Agent System Started!")
    print("Type 'exit' to quit.\n")

    while True:
        user_input = input("👩‍💻 You: ")
        if user_input.strip().lower() in ["exit", "quit"]:
            print("👋 Exiting. Thank you!")
            break

        # ==== Ask for dynamic context ====
        name = input("🧑 What is your name? ").strip().title()
        issue_type = input("🔧 Enter issue type (technical / billing / refund): ").strip().lower()
        premium_input = input("💎 Are you a premium user? (yes / no): ").strip().lower()
        is_premium = premium_input in ["yes", "y"]

        user_data = user_info(
            name=name,
            is_premium=is_premium,
            issue_type=issue_type
        )

        print(f"\n🤖 Hi {name}, let me assist you...\n")

        async for event in Runner.run_streamed(
            agent=support_agent,
            input=user_input,
            context=user_data,
            config=config
        ):
            if hasattr(event, "name") and event.name:
                print(f"\n🛠️ Event Triggered: {event.name}")
            if hasattr(event, "delta") and event.delta:
                print(event.delta, end="", flush=True)

        print("\n" + "-" * 60 + "\n")

# ================= Entry ================================
if __name__ == "__main__":
    asyncio.run(main())
