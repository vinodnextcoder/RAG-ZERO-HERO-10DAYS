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

# 3️⃣ Create client
client = OpenAI(
    base_url="https://openrouter.ai/api/v1",
    api_key=api_key,
)
# Few-Shot Learning Templates
def build_few_shot_prompt(instruction: str, prompt: str):

    # 3️⃣ Build system persona message
    system_message = (
        f"Respond strictly as per  {instruction}."
    )

    # 4️⃣ User message remains the raw prompt
    user_message = prompt.strip()

    try:
        response = client.chat.completions.create(
            model="openai/gpt-oss-20b:free",
            messages=[
                {"role": "system", "content": system_message},
                {"role": "user", "content": user_message}
            ],
        )

        return response.choices[0].message.content

    except Exception as e:
        print("❌ API call failed:", e)
        return None


# ▶️ Example usage
if __name__ == "__main__":
    classification_instruction = "Classify customer reviews as Positive, Negative, or Neutral."
    prompt ="I love the new design of your website!"
    answer = build_few_shot_prompt(classification_instruction, prompt)
    if answer:
        print("\n🟢 Response:")
        print(answer)
