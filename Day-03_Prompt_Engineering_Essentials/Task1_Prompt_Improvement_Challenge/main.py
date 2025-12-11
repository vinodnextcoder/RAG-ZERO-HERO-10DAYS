# task1_prompt_improvements.py

from openai import OpenAI
import os

api_key = os.getenv("OPENROUTER_API_KEY")

if not api_key:
    raise ValueError("OPENROUTER_API_KEY not set in environment")

# --- Initialize client once ---
client = OpenAI(base_url="https://openrouter.ai/api/v1", api_key=api_key)

# --- Prompts with example content and explanation of improvement ---
prompts = [
    {
        "id": "1",
        "old_prompt": "Tell me about machine learning",
        "improved_prompt": (
            "Explain machine learning in simple terms for beginners, including:\n"
            "1. Definition\n2. How it works\n3. 3 real-world examples"
        ),
        "why_improved": "Specifies audience, structure, and real examples, making the model's answer clearer and more useful."
    },
    {
        "id": "2",
        "old_prompt": "Fix this code",
        "improved_prompt": (
            "Identify and correct errors in the following Python code and explain the fix:\n"
            "```python\na = 5\nb = '10'\nprint(a + b)\n```"
        ),
        "why_improved": "Includes actual code and requests explanation, allowing the model to provide a correct and informative answer."
    },
    {
        "id": "3",
        "old_prompt": "Summarize this",
        "improved_prompt": (
            "Summarize the following paragraph in 3-4 bullet points, focusing only on the main ideas:\n"
            "'Artificial intelligence is transforming industries by automating tasks, improving decision-making, and enabling new capabilities.'"
        ),
        "why_improved": "Specifies the text to summarize, number of bullet points, and focus, producing a concise, structured summary."
    },
    {
        "id": "4",
        "old_prompt": "What's the best way to learn programming?",
        "improved_prompt": (
            "List 3 effective strategies for a beginner to learn programming within 30 days, including resources and weekly plan."
        ),
        "why_improved": "Clarifies timeframe, audience, and output format, making the response actionable and step-by-step."
    },
    {
        "id": "5",
        "old_prompt": "Explain this document",
        "improved_prompt": (
            "Summarize the key points and implications of the following document in simple language:\n"
            "'Data privacy policies define how companies collect, store, and use customer information.'"
        ),
        "why_improved": "Includes the document text and specifies simplification, making it understandable for non-technical readers."
    },
]

responses = []

# --- Main loop: Test both old and improved prompts ---
for prompt in prompts:
    print(f"\n===== Processing Prompt ID {prompt['id']} =====")

    system_message = "You are a helpful assistant that answers user questions fully and clearly."

    try:
        # Test old prompt
        resp_old = client.chat.completions.create(
            model="gpt-4o-mini",
            messages=[
                {"role": "system", "content": system_message},
                {"role": "user", "content": prompt["old_prompt"]}
            ],
            temperature=0.1
        )

        # Test improved prompt
        resp_new = client.chat.completions.create(
            model="gpt-4o-mini",
            messages=[
                {"role": "system", "content": system_message},
                {"role": "user", "content": prompt["improved_prompt"]}
            ],
            temperature=0.1
        )

        responses.append({
            "id": prompt["id"],
            "old_prompt": prompt["old_prompt"],
            "response_old": resp_old.choices[0].message.content,
            "improved_prompt": prompt["improved_prompt"],
            "why_improved": prompt["why_improved"],
            "response_new": resp_new.choices[0].message.content
        })

    except Exception as e:
        print(f"❌ API call failed for Prompt ID {prompt['id']}: {e}")

# --- Summary: Compare old vs improved prompts ---
for resp in responses:
    print(f"\n--- Prompt ID: {resp['id']} ---")

    print(f"\n🟥 Old Prompt:\n{resp['old_prompt']}")
    print(f"\n🔻 Response to Old Prompt:\n{resp['response_old']}")

    print(f"\n🟩 Improved Prompt:\n{resp['improved_prompt']}")
    print(f"\nWhy Improved: {resp['why_improved']}")
    print(f"\n🔺 Response to Improved Prompt:\n{resp['response_new']}")

    print("\n" + "-"*70 + "\n")
