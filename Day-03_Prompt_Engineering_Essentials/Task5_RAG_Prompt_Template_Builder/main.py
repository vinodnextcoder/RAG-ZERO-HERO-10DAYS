import json
from openai import OpenAI
import os
import sys
from dotenv import load_dotenv

load_dotenv()
class RAGPromptBuilder:
    def __init__ (self,file_path):

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
        self.client = OpenAI(
            base_url="https://openrouter.ai/api/v1",
            api_key=api_key,
        )
        self.file_path = file_path
        print(f"DocumentManager initialized with file: {self.file_path}")
        self.content = ""

    def add_context(self):
        print("Loading document...")
        print(f"File path: {self.file_path}")
        try:
            with open(self.file_path, 'r', encoding='utf-8') as file:
                self.content = file.read()
        except FileNotFoundError:
            print(f"The file at {self.file_path} does not exist.")
        except Exception as e:
            print(f"An error occurred: {e}")

    def build_response_prompt(self, system_message: str, user_message: str):
        # 4️⃣ User message remains the raw prompt
        user_message = user_message.strip()

        try:
            response = self.client.chat.completions.create(
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
    
    def context_injection_pattern(self, user_question: str):
        prompt_template = f"""
        You are an AI assistant that uses the following context to answer user queries.

        Context:
        {self.content}

        Instructions:
        - Use the provided context to answer the user's question.
        - If the context does not contain the answer, respond with "I don't know."

        User Question:
        {{user_question}}

        Answer:
        """
        prompt_template = self.build_response_prompt(prompt_template, user_question)
        return prompt_template






builder = RAGPromptBuilder("sample.txt")
builder.add_context()
response_context_injection_pattern_1 = builder.context_injection_pattern("what is ModuleNotFoundError in python?")
print("\n🟢 Response: 1")
print(response_context_injection_pattern_1)
response_context_injection_pattern_2 = builder.context_injection_pattern("what is movie")
print("\n🟢 Response: 2")
print(response_context_injection_pattern_2)
# doc.search_documents("chunking")
# result = doc.calculate_document_statistics()
# print("\nReturned Statistics Dictionary:")
# print(result)
# print("Document processing completed.")
# export_to_json(result, "document_statistics.json")