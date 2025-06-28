🛠️ Tool Function
python
Copy
Edit
@function_tool
def get_weather(city: str) -> Weather:
    return Weather(city=city, temperature_range="14-20C", conditions="Sunny with wind.")
🧠 Agent Setup
python
Copy
Edit
agent = Agent(
    name="Hello world",
    instructions="You are a helpful agent.",
    tools=[get_weather],
)
▶️ Run the Agent
python
Copy
Edit
result = await Runner.run(agent, input="What's the weather in Tokyo?")
print(result.final_output)
✅ Sample Output
pgsql
Copy
Edit
[debug] get_weather called
The weather in Tokyo is sunny with wind. Temperature is between 14-20C.