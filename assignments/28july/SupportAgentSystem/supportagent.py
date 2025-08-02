# supportagent.py

import os
import asyncio
from dotenv import load_dotenv
from openai import AsyncOpenAI
from agents import (
    Agent,
    OpenAIChatCompletionsModel,
    Runner,
    RunConfig,
    RunContextWrapper,
    function_tool,
)

load_dotenv()

# ============ Base Config ==============
client = AsyncOpenAI()
model = OpenAIChatCompletionsModel(client=client, model="gpt-4o")

# ============ Context Schema ===========
from pydantic import BaseModel

class user_info(BaseModel):
    name: str
    is_premium: bool
    issue_type: str  # technical, billing, refund

# ============ Tools ====================

@function_tool(name="check_account_status")
async def check_account_status(ctx: RunContextWrapper):
    user = ctx.inputs["user_info"]
    if user.is_premium:
        return f"{user.name} is a premium user. Handle with priority. 🎖️"
    else:
        return f"{user.name} is a standard user."

@function_tool(name="check_refund_policy")
async def check_refund_policy(ctx: RunContextWrapper):
    return "Refunds are only processed within 7 days of purchase, and only for major issues."

# ============ Agents ====================

BillingAgent = Agent(
    name="BillingAgent",
    model=model,
    instructions="You are a billing support expert. Handle all billing-related issues and explain policies clearly.",
    tools=[check_account_status, check_refund_policy]
)

TechnicalAgent = Agent(
    name="TechnicalAgent",
    model=model,
    instructions="You are a tech support engineer. Help with technical issues in a simple, polite way.",
    tools=[check_account_status]
)

GeneralSupportAgent = Agent(
    name="GeneralSupportAgent",
    model=model,
    instructions="You handle all general support questions. Be polite and helpful.",
)

# ============ Triage Agent ==============

@function_tool(name="triage", return_type=str)
async def triage(ctx: RunContextWrapper):
    user = ctx.inputs["user_info"]
    if user.issue_type == "billing" or user.issue_type == "refund":
        return "BillingAgent"
    elif user.issue_type == "technical":
        return "TechnicalAgent"
    else:
        return "GeneralSupportAgent"

SupportTriageAgent = Agent(
    name="SupportTriageAgent",
    model=model,
    instructions="You decide which support agent should handle a query based on issue_type. Use the triage tool.",
    tools=[triage],
)

# ============ Runner =====================

runner = Runner(
    agents=[
        BillingAgent,
        TechnicalAgent,
        GeneralSupportAgent,
        SupportTriageAgent
    ],
    config=RunConfig(
        enable_handoff=True,
        max_handoff_depth=2,
    )
)

# ============ Entry Point =================

async def main():
    print("🤖 Welcome to the Console Support Agent System!\n")

    while True:
        try:
            # Ask for user context
            user_name = input("👤 Enter your name: ").strip()
            issue_type = input("🔧 Enter issue type (technical / billing / refund): ").strip().lower()
            premium_input = input("💎 Are you a premium user? (yes / no): ").strip().lower()
            is_premium = premium_input in ["yes", "y"]

            user_data = user_info(
                name=user_name,
                is_premium=is_premium,
                issue_type=issue_type
            )

            # Ask for user query
            user_query = input("📝 What's your question? ").strip()

            # Run the triage agent
            result = await runner.run(
                agent_name="SupportTriageAgent",
                input=user_query,
                context={"user_info": user_data},
            )

            print(f"\n💬 AI Response: {result.output}\n")

            cont = input("🔁 Do you want to ask another question? (yes / no): ").strip().lower()
            if cont not in ["yes", "y"]:
                print("👋 Goodbye!")
                break

        except Exception as e:
            print(f"❌ Error: {e}")
            break

if __name__ == "__main__":
    asyncio.run(main())




# # supportagent.py

# import os
# import asyncio
# from dotenv import load_dotenv
# from openai import AsyncOpenAI
# from agents import (
#     Agent,
#     OpenAIChatCompletionsModel,
#     Runner,
#     RunConfig,
#     RunContextWrapper,
#     function_tool,
#     input_guardrail,
#     output_guardrail,
#     GuardrailFunctionOutput,
# )
# from pydantic import BaseModel

# # ================= Load API Key ======================
# load_dotenv()
# openai_api_key = os.getenv("OPENAI_API_KEY")
# if not openai_api_key:
#     raise ValueError("OPENAI_API_KEY not found in environment variables.")

# # ================ Initialize OpenAI Client & Model ===
# client = AsyncOpenAI(api_key=openai_api_key)
# model = OpenAIChatCompletionsModel(
#     model="gpt-4o",  # or "gpt-3.5-turbo"
#     openai_client=client
# )

# # ================= Run Configuration =================
# config = RunConfig(
#     model=model,
#     tracing_disabled=True,
#     model_provider=client
# )

# # ================= Pydantic Context =====================
# class user_info(BaseModel):
#     name: str
#     is_premium: bool
#     issue_type: str  # 'technical', 'billing', 'refund'

# # ================= Tools ================================

# @function_tool(
#     is_enabled=lambda ctx, agent: ctx.context.issue_type == "refund"
# )
# def refund(ctx: RunContextWrapper[user_info]) -> str:
#     """Process a refund only if the user is premium."""
#     if ctx.context.is_premium:
#         return f"Refund processed successfully for {ctx.context.name}."
#     return f"{ctx.context.name}, you need a premium subscription to request a refund."

# @function_tool(
#     is_enabled=lambda ctx, agent: not ctx.context.is_premium
# )
# def check_issue_type(ctx: RunContextWrapper[user_info]) -> str:
#     """Return issue type to help route non-premium users."""
#     return ctx.context.issue_type

# @function_tool(
#     is_enabled=lambda ctx, agent: ctx.context.issue_type == "technical")
# def restart_service(ctx: RunContextWrapper[user_info]) -> str:
    
#     """Restart the user's service (technical support)."""
#     return f"Technical service has been restarted for {ctx.context.name}."

# # ================= Input Guardrail =========================


# class SupportIntentOutput(BaseModel):
#     is_support_related: bool
#     reasoning: str
    
    
    
# support_guardrail_agent = Agent(
#     name="Support Intent Checker",
#     instructions=(
#         "Determine whether the user is asking about a customer support issue like billing, refunds, or technical problems. "
#         "Set is_support_related = True if yes, else False. "
#         "Explain your reasoning."
#     ),
#     output_type=SupportIntentOutput,
#     model=model
# )


# @input_guardrail
# async def support_input_guardrail(
#     ctx: RunContextWrapper[None],
#     agent: Agent,
#     input: str | list[TResponseInputItem],
# ) -> GuardrailFunctionOutput:
#     result = await Runner.run(support_guardrail_agent, input, context=ctx.context)

#     return GuardrailFunctionOutput(
#         output_info=result.final_output,
#         tripwire_triggered=not result.final_output.is_support_related,
#     )

# # @input_guardrail
# # def validate_input(user_input: str) -> GuardrailFunctionOutput:
# #     blocked_phrases = ["abuse", "nonsense", "idiot", "shut up"]
# #     if any(bad_word in user_input.lower() for bad_word in blocked_phrases):
# #         return GuardrailFunctionOutput(valid=False, error="Inappropriate language is not allowed.")
# #     return GuardrailFunctionOutput(valid=True)

# # ================= Output Guardrail ========================

# class CleanSupportResponse(BaseModel):
#     contains_blocked_phrase: bool
#     reason: str
    

# blocklist_output_agent = Agent(
#     name="Blocked Phrase Checker",
#     instructions=(
#         "Check if the message contains phrases like 'I'm sorry', 'as an AI', 'LLM', or 'I cannot'. "
#         "If so, set contains_blocked_phrase=True and explain why."
#     ),
#     output_type=CleanSupportResponse,
# )

# class MessageOutput(BaseModel):
#     response: str

# @output_guardrail
# async def support_output_guardrail(
#     ctx: RunContextWrapper,
#     agent: Agent,
#     output: MessageOutput,  # this should be whatever your main agent outputs
# ) -> GuardrailFunctionOutput:
#     result = await Runner.run(blocklist_output_agent, output.response, context=ctx.context)

#     return GuardrailFunctionOutput(
#         output_info=result.final_output,
#         tripwire_triggered=result.final_output.contains_blocked_phrase,
#     )


# # @output_guardrail
# # def restrict_apologies(output: str) -> GuardrailFunctionOutput:
# #     forbidden_phrases = ["sorry", "apologize", "unfortunately"]
# #     if any(phrase in output.lower() for phrase in forbidden_phrases):
# #         return GuardrailFunctionOutput(valid=False, error="No apology phrases allowed in output.")
# #     return GuardrailFunctionOutput(valid=True)

# # ================= Main CLI App ============================
# async def main():
#     # Specialized Agents
#     technical_agent = Agent(
#         name="technical_agent",
#         instructions="You handle technical issues like restarting services, bugs, or errors.",
#         tools=[restart_service]
#     )

#     billing_agent = Agent(
#         name="billing_agent",
#         instructions="You handle billing questions including payments and charges."
#     )

#     refund_agent = Agent(
#         name="refund_agent",
#         instructions="You handle refund-related queries. Only serve premium users.",
#         tools=[refund]
#     )

#     # Triage Agent
#     support_agent = Agent(
#         name="customer_support_agent",
#         instructions="""
#     You are a helpful and polite customer support triage agent.

#     Your job is to:
#     - Read the context.issue_type (technical, billing, refund).
#     - Based on that, call the `handoff()` function to pass the conversation to the correct agent:
#         - If it's 'technical', handoff to 'technical_agent'
#         - If it's 'billing', handoff to 'billing_agent'
#         - If it's 'refund', handoff to 'refund_agent'

#     Never respond directly. Always use handoff() or tools to handle the issue.
#     """,
#         handoffs=[technical_agent, billing_agent, refund_agent],
#         handoff_description="Delegate to the correct agent using issue_type in context.",
#         tools=[check_issue_type],
#          input_guardrails=[support_input_guardrail],
#         output_guardrails=[support_output_guardrail],
#         output_type=MessageOutput,
# )
    
#     print("\n📞 Console Support Agent System Started!")
#     print("Type 'exit' to quit.\n")

#     while True:
#         user_input = input("💬 User Input: ")
#         if user_input.strip().lower() in ["exit", "quit"]:
#             print("👋 Exiting. Thank you!")
#             break

#         # Ask for user context
#         issue_type = input("🔧 Enter issue type (technical / billing / refund): ").strip().lower()
#         premium_input = input("💎 Are you a premium user? (yes / no): ").strip().lower()
#         is_premium = premium_input in ["yes", "y"]

#         user_data = user_info(
#             name="Maryam",
#             is_premium=is_premium,
#             issue_type=issue_type
#         )
       

#         print("\n🤖 Agent response:\n")

#         result = await Runner.run_streamed(
#         support_agent,
#         input=user_input ,
#         context=user_data,
#         run_config=config
#             )
#         print(result.final_output)

#     async for event in result.stream():
#         if hasattr(event, "name") and event.name:
#             print(f"\n🛠️ Event Triggered: {event.name}")
#         if hasattr(event, "delta") and event.delta:
#             print(event.delta, end="", flush=True)
#             print("\n" + "-" * 60 + "\n")


# # ================= Entry ================================
# if __name__ == "__main__":
#     asyncio.run(main())