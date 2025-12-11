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
    print("👉 Please set it in environment variables or in a .env file.")
    print("👉 Example:")
    print("   export OPENROUTER_API_KEY='your_api_key_here'  (Linux/macOS)")
    print("   setx OPENROUTER_API_KEY \"your_api_key_here\"   (Windows)")
    sys.exit(1)

# 3️⃣ Define prompts
prompts = [
    {
        "id": "1",
        "old_prompt": "Tell me about machine learning",
        "improved_prompt": (
            "Explain machine learning in 3 sentences, focusing on:\n"
            "1. What it's used for\n"
            "2. Why it's popular for AI"
        ),
    },
    {
        "id": "2",
        "old_prompt": "Fix this code",
        "improved_prompt": "Identify and correct the syntax error in the following Python code snippet:",
    },
    {
        "id": "3",
        "old_prompt": "Summarize this",
        "improved_prompt": "Summarize the following legal text in 4-5 bullet points with only key insights.",
    },
    {
        "id": "4",
        "old_prompt": "What's the best way to learn programming?",
        "improved_prompt": "List 3 effective strategies for beginners to learn programming, including resources.",
    },
    {
        "id": "5",
        "old_prompt": "Explain this document",
        "improved_prompt": "Summarize the terms and implications of the following document in simple language.",
    },
]

responses = []

# 4️⃣ Main loop
for prompt in prompts:
    print(f"\n===== Processing Prompt ID {prompt['id']} =====")

    client = OpenAI(
        base_url="https://openrouter.ai/api/v1",
        api_key=api_key,
    )

    try:
        # Request 1 (Old prompt)
        chat_completion_1 = client.chat.completions.create(
            model="openai/gpt-oss-20b:free",
            messages=[
                {
                    "role": "system",
                    "content": (
                        "If the user prompt is incomplete, ask for missing details instead of answering."
                    )
                },
                {"role": "user", "content": prompt["old_prompt"]}
            ],
            temperature=0.1
        )

        # Request 2 (Improved prompt)
        chat_completion_2 = client.chat.completions.create(
            model="openai/gpt-oss-20b:free",
            messages=[
                {
                    "role": "system",
                    "content": (
                        "If the user prompt is incomplete, ask for missing details instead of answering."
                    )
                },
                {"role": "user", "content": prompt["improved_prompt"]}
            ],
            temperature=0.1
        )

        responses.append({
            "id": prompt["id"],
            "old_prompt": prompt["old_prompt"],
            "response_1": chat_completion_1.choices[0].message.content,
            "improved_prompt": prompt["improved_prompt"],
            "response_2": chat_completion_2.choices[0].message.content,
        })

    except Exception as e:
        print(f"❌ API call failed for ID {prompt['id']} — Reason: {e}")

# 5️⃣ Summary Output
print("\n\n======================== SUMMARY OF RESPONSES ========================\n")

for resp in responses:
    print(f"--- Prompt ID: {resp['id']} ---")
    print(f"\n🟥 Old Prompt:")
    print(resp["old_prompt"])
    print(f"\n🔻 Model Response (Old Prompt):")
    print(resp["response_1"])

    print("\n🟩 Improved Prompt:")
    print(resp["improved_prompt"])
    print(f"\n🔺 Model Response (Improved Prompt):")
    print(resp["response_2"])

    print("\n" + "-" * 70 + "\n")
