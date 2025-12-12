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
    print('   setx OPENROUTER_API_KEY "your_api_key_here"   (Windows)')
    sys.exit(1)

# 3️⃣ Create client
client = OpenAI(
    base_url="https://openrouter.ai/api/v1",
    api_key=api_key,
)


# Few-Shot Learning Templates
def solve_problem(prompt: str):

    system_prompt = """
        You are a careful, stepwise problem solver.

        For every problem:
        - Produce a short, concise reasoning summary (3-6 high-level steps).
        - Do NOT reveal hidden chain-of-thought. Only summarize the main steps.
        - Then output a clearly labeled "Final answer".
        - Use this exact format:

        Reasoning summary:
        1) ...
        2) ...
        3) ...

        Final answer: ...
        """

            # 4️⃣ User message remains the raw prompt
    user_prompt = f"""
        Task: Solve the following problem.

        1) Provide a concise numbered "Reasoning summary" (3–6 high-level steps).
        2) Then give a single-line "Final answer".

        Problem:
        {prompt.strip()}

        Format required exactly:
        Reasoning summary:
        1) ...
        2) ...
        3) ...

        Final answer: ...
        """

    try:
        response = client.chat.completions.create(
            model="openai/gpt-oss-20b:free",
            messages=[
                {"role": "system", "content": system_prompt},
                {"role": "user", "content": user_prompt},
            ],
        )

        return response.choices[0].message.content

    except Exception as e:
        print("❌ API call failed:", e)
        return None


# ▶️ Example usage
if __name__ == "__main__":

    prompt = "A shop sells 3 pencils for ₹50. How much for 20 pencils?"
    answer = solve_problem(prompt)
    if answer:
        print("\n🟢 Response:")
        print(answer)
