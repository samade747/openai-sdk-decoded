# 🖼️ OpenAI Agent – Image Input via URL Example

This example shows how to send an **image via URL** to an OpenAI Agent using the [OpenAI Python Agents SDK](https://github.com/openai/openai-agents-python), and then ask a follow-up question.

---

## 🧠 What It Demonstrates

✅ Send an image to the assistant using a public URL  
✅ Ask a natural language question based on the image  
✅ Process multi-turn messages (image ➝ question)

---

## 📷 Image Used

[Golden Gate Bridge – Wikimedia Commons](https://upload.wikimedia.org/wikipedia/commons/0/0c/GoldenGateBridge-001.jpg)

---

## 📦 Requirements

- Python 3.8+
- OpenAI Python Agents SDK
- Internet access (for downloading the image from URL)

---

## ▶️ How to Run

```bash
python image_input_url_example.py



import asyncio
from agents import Agent, Runner

URL = "https://upload.wikimedia.org/wikipedia/commons/0/0c/GoldenGateBridge-001.jpg"

async def main():
    agent = Agent(
        name="Assistant",
        instructions="You are a helpful assistant.",
    )

    result = await Runner.run(
        agent,
        [
            {
                "role": "user",
                "content": [
                    {
                        "type": "input_image",
                        "detail": "auto",
                        "image_url": URL,
                    }
                ],
            },
            {
                "role": "user",
                "content": "What do you see in this image?",
            },
        ],
    )
    print(result.final_output)

if __name__ == "__main__":
    asyncio.run(main())
