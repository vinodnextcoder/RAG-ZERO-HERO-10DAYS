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

# ✅ 4️⃣ Function to send user-defined role & prompt
def ask_model(role: str, prompt: str):
    """
    Sends a chat completion request where:
      - `role` = persona (e.g., "Python tutor", "doctor", "pirate captain")
      - `prompt` = user query

    Validations:
      - If role missing -> politely refuse.
      - If prompt missing -> politely refuse.

    Behavior:
      - Combines both into a system + user message for proper role-playing.
    """

    # 1️⃣ Validate role
    if not role or role.strip() == "":
        return (
            "❌ I didn't receive a valid role/persona.\n"
            "Please provide one, for example:\n"
            "\"Python tutor\", \"doctor\", \"cybersecurity expert\", \"pirate captain\""
        )

    # 2️⃣ Validate prompt
    if not prompt or prompt.strip() == "":
        return (
            "❌ I didn't receive a prompt.\n"
            "Please provide something like:\n"
            "\"Explain variables to a beginner programmer.\""
        )

    # 3️⃣ Build system persona message
    system_message = (
        f"You are an expert {role}. "
        f"Respond strictly in role-playing style as a(n) {role}."
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
    answer = ask_model("user", "Explain Python in one line.")
    if answer:
        print("\n🟢 Response:")
        print(answer)
