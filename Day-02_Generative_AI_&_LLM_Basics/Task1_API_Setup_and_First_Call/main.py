import os
import sys
from openai import OpenAI
from dotenv import load_dotenv
load_dotenv()


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


# 3️⃣ Create client only if key exists
client = OpenAI(
    base_url="https://openrouter.ai/api/v1",
    api_key=api_key,
)

# 4️⃣ Make request
try:
    chat_completion = client.chat.completions.create(
        model="openai/gpt-oss-20b:free",
        messages=[
            {"role": "user", "content": "What is Python?"}
        ],
    )

    print(chat_completion.choices[0].message.content)

except Exception as e:
    print("❌ API call failed")
    print(f"Reason: {e}")
