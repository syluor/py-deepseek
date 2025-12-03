from openai import OpenAI

def send_messages(messages):
    response = client.chat.completions.create(
        model="deepseek-chat",
        messages=messages,
        tools=tools
    )
    return response.choices[0].message

client = OpenAI(
    api_key="sk-2b84539cb0a846bab2977ba5ed0548f4sk-2b84539cb0a846bab2977ba5ed0548f4",
    base_url="https://api.deepseek.com",
)

tools = [
    {
        "type": "function",
        "function": {
            "name": "get_weather",
            "description": "Get weather of a location, the user should supply a location first.",
            "parameters": {
                "type": "object",
                "properties": {
                    "location": {
                        "type": "string",
                        "description": "The city and state, e.g. San Francisco, CA",
                    }
                },
                "required": ["location"]
            },
        }
    },
]

if __name__ == "__main__":
    messages = [{"role": "user", "content": "How's the weather in Hangzhou, Zhejiang?"}]
    message = send_messages(messages)
    print(f"User>\t {messages[0]['content']}")

    tool = message.tool_calls[0]
    messages.append(message)

    messages.append({"role": "tool", "tool_call_id": tool.id, "content": "24℃"})
    message = send_messages(messages)
    print(f"Model>\t {message.content}")
