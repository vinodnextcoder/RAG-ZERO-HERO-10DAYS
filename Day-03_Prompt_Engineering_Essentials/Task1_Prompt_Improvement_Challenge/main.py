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
prompts = [{
    "id": "1",
    "old_prompt": "Tell me about machine learning",
    "improved_prompt": """Explain machine learning in 3 sentences, focusing on:
        1. What it's used for
        2. Why it's popular for AI""",
    },
    {
    "id": "2",
    "old_prompt": "Fix this code",
    "improved_prompt": "Identify and correct the syntax error in the following Python code snippet: ",
    },
    {
    "id": "3",
    "old_prompt": "Summarize this",
    "improved_prompt": "Summarize the following legal in 4-5 bullet points, keeping only the key arguments and main insights.",
    },
    {
    "id": "4",
    "old_prompt": "What's the best way to learn programming?",
    "improved_prompt": "List 3 effective strategies for beginners to learn programming, including resources and practice methods.",
    },
    {
    "id": "5",
    "old_prompt": "Explain this document",
    "improved_prompt": "Summarize the terms and implications of the following document in simple language suitable for a non-expert audience.",
    },
    {
    "id": "6",
    "old_prompt": "Explain this document",
    "improved_prompt": "Summarize the key legal terms and implications of the following document in simple language suitable for a non-expert audience.",
    },
    {
    "id": "7",
    "old_prompt": "Fix this code :def add_numbers(a, b): print(\"Adding numbers...\"); result = a + b; return result; x = 10;  = add_numbers(x, y); print(\"Sum:\", sum)",
    "improved_prompt": "Identify and correct the syntax error in the following Python code snippet: def add_numbers(a, b): print(\"Adding numbers...\"); result = a + b; return result; x = 10;  sum = add_numbers(x, y);  sum)",
    }
]
   


responses = []
for prompt in prompts:
    print(prompt)
    # print(f"\n--- Temperature: {prompt["id"]} ---")
    print(f"\n--- Temperature: {prompt['id']} ---")
    client = OpenAI(
        base_url="https://openrouter.ai/api/v1",
        api_key=api_key,
    )

    # 4️⃣ Make request
    try:
        chat_completion_1 = client.chat.completions.create(
            model="openai/gpt-oss-20b:free",
            messages=[
                    {
                        "role": "system",
                        "content": (
                            "You must not answer any question unless the user has provided all required "
                            "information. If the user's input is incomplete or unclear, ask for the exact "
                            "missing details and do not answer until all details are available."
                        )
                    },
                    {"role": "user", "content": prompt["old_prompt"]}  # incomplete → model will ask details
                ],
            temperature=0.1
        )
        chat_completion_2 = client.chat.completions.create(
            model="openai/gpt-oss-20b:free",
            messages=[
                    {
                        "role": "system",
                        "content": (
                            "You must not answer any question unless the user has provided all required "
                            "information. If the user's input is incomplete or unclear, ask for the exact "
                            "missing details and do not answer until all details are available."
                        )
                    },
                    {"role": "user", "content": prompt["improved_prompt"]}  # incomplete → model will ask details
                ],
            temperature=0.1
        )

        # print(chat_completion.choices[0].message.content)
        responses.append({
            "id": prompt["id"],
            "old_prompt": prompt["old_prompt"],
            "improved_prompt": prompt["improved_prompt"],
            "response_1": chat_completion_1.choices[0].message.content,
            "response_2": chat_completion_2.choices[0].message.content,  
        })

    except Exception as e:
        print("❌ API call failed")
        print(f"Reason: {e}")

print("\n\n=== Summary of Responses ===")
for resp in responses:
    print(f"\n--- Prompt ID: {resp['id']} ---")
    print(f"Old Prompt: {resp['old_prompt']}")
    print(f"Response 1: {resp['response_1']}")
    print(f"Improved Prompt: {resp['improved_prompt']}")
    print(f"Response 2: {resp['response_2']}")
