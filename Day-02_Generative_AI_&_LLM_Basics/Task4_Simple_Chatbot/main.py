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

    assistant_message = response.choices[0].message.content
    print(f"\n🤖 Assistant: {assistant_message}")

    messages.append({"role": "assistant", "content": assistant_message})
    return assistant_message, messages


# ============================
#   INTERACTIVE CHAT LOOP
# ============================

def start_chat():
    print("💬 Simple Chatbot with Memory")
    print("--------------------------------------")
    print("Type your messages below.")
    print("Commands:")
    print(" - 'clear' or 'reset' to clear history")
    print(" - 'quit' or 'exit' to stop\n")

    conversation = []

    while True:
        user_input = input("👤 You: ").strip()

        # Exit command
        if user_input.lower() in ["quit", "exit"]:
            print("👋 Exiting chat. Goodbye!")
            break

        # Clear conversation
        if user_input.lower() in ["clear", "reset"]:
            conversation = []
            print("🧹 Conversation history cleared!")
            continue

        # Normal conversation
        _, conversation = chat_with_context(conversation, user_input)


# Run the chatbot
if __name__ == "__main__":
    start_chat()
