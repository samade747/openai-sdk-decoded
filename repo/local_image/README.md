import asyncio
import base64
import os
from agents import Agent, Runner

# 🔍 Path to image file
FILEPATH = os.path.join(os.path.dirname(__file__), "media/image_bison.jpg")

# 🖼️ Convert image to base64 for use in messages
def image_to_base64(image_path):
    with open(image_path, "rb") as image_file:
        encoded_string = base64.b64encode(image_file.read()).decode("utf-8")
    return encoded_string

# 🚀 Main function to run the agent
async def main():
    # Convert the image to a base64 string
    b64_image = image_to_base64(FILEPATH)

    # Define the agent with basic instructions
    agent = Agent(
        name="Assistant",
        instructions="You are a helpful assistant.",
    )

    # Provide the image and follow-up question as user messages
    result = await Runner.run(
        agent,
        [
            {
                "role": "user",
                "content": [
                    {
                        "type": "input_image",
                        "detail": "auto",
                        "image_url": f"data:image/jpeg;base64,{b64_image}",
                    }
                ],
            },
            {
                "role": "user",
                "content": "What do you see in this image?",
            },
        ],
    )

    # Output the assistant's response
    print(result.final_output)

# 🟢 Run the async agent
if __name__ == "__main__":
    asyncio.run(main())
