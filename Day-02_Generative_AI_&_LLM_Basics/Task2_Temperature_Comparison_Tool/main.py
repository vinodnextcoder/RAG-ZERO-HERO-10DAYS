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
tempature = [0.1, 0.7, 1.5]
responses = []
for t in tempature:
    print(f"\n--- Temperature: {t} ---")
    client = OpenAI(
        base_url="https://openrouter.ai/api/v1",
        api_key=api_key,
    )

    # 4️⃣ Make request
    try:
        chat_completion = client.chat.completions.create(
            model="openai/gpt-oss-20b:free",
            messages=[
                {"role": "user", "content": "Write a haiku about coding"}
            ],
        )

        # print(chat_completion.choices[0].message.content)
        responses.append({
            "temperature": t,
            "response": chat_completion.choices[0].message.content
        })

    except Exception as e:
        print("❌ API call failed")
        print(f"Reason: {e}")

# 5️⃣ Display all responses
print("\n=== Summary of Responses ===")

print(f"{'Temperature':<15} | Response")
print("-" * 70)

for resp in responses:
    print(f"{resp['temperature']:<15} | {resp['response']}")
