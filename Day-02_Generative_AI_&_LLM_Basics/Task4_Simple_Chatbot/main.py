import os
import sys
from openai import OpenAI
from dotenv import load_dotenv

load_dotenv()

def chat_with_context(messages, user_message):
    """Maintain conversation context"""
    messages.append({"role": "user", "content": user_message})

    # 1️⃣ Read API key
    api_key = os.getenv("OPENROUTER_API_KEY")

    # 2️⃣ Handle missing key
    if not api_key:
        print("❌ ERROR: OPENROUTER_API_KEY not found.")
        print("👉 Please set it as an environment variable or in a .env file.")
        print("👉 Example:")
        print("   export OPENROUTER_API_KEY='your_api_key_here'  (Linux/macOS)")
        print("   setx OPENROUTER_API_KEY \"your_api_key_here\"   (Windows)")
        sys.exit(1)

    # 3️⃣ Create correct client
    client = OpenAI(
        base_url="https://openrouter.ai/api/v1",
        api_key=api_key
    )

    # 4️⃣ Make request
    response = client.chat.completions.create(
        model="openai/gpt-oss-20b:free",
        messages=messages
    )
    print("Response received.",response.choices[0].message.content)
    assistant_message =  response.choices[0].message.content
    messages.append({"role": "assistant", "content": assistant_message})

    return assistant_message, messages


# Usage
conversation = []
response, conversation = chat_with_context(
    conversation, 
    "My name is Alice"
)
response, conversation = chat_with_context(
    conversation,
    "What's my name?"  # Model remembers context!
)
