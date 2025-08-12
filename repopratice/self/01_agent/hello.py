
# import os
# import asyncio
# from dotenv import load_dotenv

# from agents import Agent, Runner, AsyncOpenAI, OpenAIChatCompletionsModel
# from agents.run import RunConfig

# # Load environment variables
# load_dotenv()
# gemini_api_key = os.getenv("GEMINI_API_KEY")

# if not gemini_api_key:
#     raise ValueError("GEMINI_API_KEY is not set in .env file")

# # Set up Gemini client
# external_client = AsyncOpenAI(
#     api_key=gemini_api_key,
#     base_url="https://generativelanguage.googleapis.com/v1beta/openai/"
# )

# # Define model
# model = OpenAIChatCompletionsModel(
#     model="gemini-2.0-flash",
#     openai_client=external_client
# )

# # Configuration
# config = RunConfig(
#     model=model,
#     model_provider=external_client,
#     tracing_disabled=True
# )



# # import asyncio
# # import os

# # from dotenv import load_dotenv, find_dotenv
# # from agents import Agent, Runner, OpenAIChatCompletionsModel, AsyncOpenAI

# # load_dotenv(find_dotenv())

# # provider = AsyncOpenAI(base_url="https://api.openai.com/v1",
# #                        api_key=os.getenv("OPENAI_API_KEY"))


# async def main():
#     agent = Agent(
#         name="Assistant",
#         instructions="You only respond in eng.",
#         model=OpenAIChatCompletionsModel(
#             openai_client=external_client, model="gpt-4o-mini"),

#     )

#     result = await Runner.run(agent, "Tell me about agents!")
#     print(result.final_output)
#     # Function calls itself,
#     # Looping in smaller pieces,
#     # Endless by design.


# if __name__ == "__main__":
#     print("\n[STARTING AGENT]\n")
#     asyncio.run(main())


import asyncio
import os

from dotenv import load_dotenv, find_dotenv
from agents import Agent, Runner, OpenAIChatCompletionsModel, AsyncOpenAI

load_dotenv(find_dotenv())

provider = AsyncOpenAI(base_url="https://api.openai.com/v1",
                       api_key=os.getenv("OPENAI_API_KEY"))


async def main():
    agent = Agent(
        name="Assistant",
        instructions="You only respond in eng.",
        model=OpenAIChatCompletionsModel(
            openai_client=provider, model="gpt-4o-mini"),

    )

    result = await Runner.run(agent, "Tell me about agents!")
    print(result.final_output)
    # Function calls itself,
    # Looping in smaller pieces,
    # Endless by design.


if __name__ == "__main__":
    print("\n[STARTING AGENT]\n")
    asyncio.run(main())