import asyncio
from agents import Agent, Runner

# 📸 URL of an input image (Golden Gate Bridge)
URL = "https://upload.wikimedia.org/wikipedia/commons/0/0c/GoldenGateBridge-001.jpg"

async def main():
    # Create the agent
    agent = Agent(
        name="Assistant",
        instructions="You are a helpful assistant.",
    )

    # Send the image first, followed by a text question
    result = await Runner.run(
        agent,
        [
            {
                "role": "user",
                "content": [
                    {
                        "type": "input_image",         # ⬅️ this is required for image
                        "detail": "auto",              # 'auto' lets the model choose detail level
                        "image_url": URL,              # ⬅️ Image is referenced by URL
                    }
                ],
            },
            {
                "role": "user",
                "content": "What do you see in this image?",  # ⬅️ Follow-up user message
            },
        ],
    )

    # Show the agent's response
    print(result.final_output)

# 🔁 Run async main function
if __name__ == "__main__":
    asyncio.run(main())
