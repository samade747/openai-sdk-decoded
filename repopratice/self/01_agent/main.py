from agents import Agent, Runner, AsyncOpenAI, OpenAIChatCompletionsModel, RunConfig
from dotenv import load_dotenv
import os

# Load environment variables
load_dotenv()
gemini_api_key = os.getenv("GEMINI_API_KEY")

if not gemini_api_key:
    raise ValueError("GEMINI_API_KEY is not set. Please ensure it is defined in your .env file.")

# Setup Gemini client
external_client = AsyncOpenAI(
    api_key=gemini_api_key,
    base_url="https://generativelanguage.googleapis.com/v1beta/openai/",
)

model = OpenAIChatCompletionsModel(
    model="gemini-2.0-flash",
    openai_client=external_client
)

config = RunConfig(
    model=model,
    model_provider=external_client,
    tracing_disabled=True
)

# 🧠 Translator Agent
translator = Agent(
    name="Urdu-English Translator",
    instructions=(
        "You are a translation expert. Translate the given text accurately. "
        "If the prompt says 'Translate to Urdu', return the Urdu translation. "
        "If the prompt says 'Translate to English', return the English translation."
    ),
)

def run_translator():
    print("🌐 Urdu ↔ English Translator")
    print("Choose translation direction:")
    print("1. English to Urdu")
    print("2. Urdu to English")

    choice = input("Enter 1 or 2: ")

    if choice not in ("1", "2"):
        print("❌ Invalid choice. Please enter 1 or 2.")
        return

    text = input("Enter the text to translate: ")

    if choice == "1":
        prompt = f"Translate to Urdu: \"{text}\""
    else:
        prompt = f"Translate to English: \"{text}\""

    response = Runner.run_sync(
        translator,
        input=prompt,
        run_config=config
    )

    print("\n🔁 Translated Text:")
    print(response.final_output)

run_translator()
