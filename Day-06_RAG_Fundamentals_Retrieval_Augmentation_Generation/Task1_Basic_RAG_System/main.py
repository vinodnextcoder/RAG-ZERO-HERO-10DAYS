from openai import OpenAI
import os, sys
import chromadb
from chromadb.config import Settings
import os
from dotenv import load_dotenv

load_dotenv()


class SimpleRAG:
    def __init__(self):
        self.client = chromadb.Client(Settings())
        self.collection = None
        # 1️⃣ Read API key
        self.api_key = os.getenv("OPENROUTER_API_KEY")

        # 2️⃣ Handle missing key
        if not self.api_key:
            print("❌ ERROR: OPENROUTER_API_KEY not found.")
            print("👉 Please set it as an environment variable or in a .env file.")
            print("👉 Example:")
            print("   export OPENROUTER_API_KEY='your_api_key_here'  (Linux/macOS)")
            print('   setx OPENROUTER_API_KEY "your_api_key_here"   (Windows)')
            sys.exit(1)

        # 3️⃣ Create client only if key exists
        self.client_openai = OpenAI(
            base_url="https://openrouter.ai/api/v1",
            api_key=self.api_key,
        )

    def setup(self, collection_name="documents"):
        """Initialize collection"""
        self.collection = self.client.create_collection(name=collection_name)

    def add_documents(self, texts, ids=None, metadatas=None):
        """Add documents to the collection"""
        if ids is None:
            ids = [f"doc_{i}" for i in range(len(texts))]

        self.collection.add(documents=texts, ids=ids, metadatas=metadatas)

    def retrieve(self, query, k=3):
        """Retrieve top K relevant chunks"""
        results = self.collection.query(query_texts=[query], n_results=k)
        return results["documents"][0]

    def augment(self, context_chunks, question):
        """Create augmented prompt"""
        context = "\n\n".join(
            [f"[Document {i+1}]\n{chunk}" for i, chunk in enumerate(context_chunks)]
        )
        prompt = f"""Use the following documents to answer the question.

        Documents:
        {context}

        Question: {question}

        Answer based only on the provided documents. If the documents don't contain enough information, say so."""

        return prompt

    def generate(self, prompt):
        """Generate answer using LLM"""
        response = self.client_openai.chat.completions.create(
            model="openai/gpt-oss-20b:free",
            messages=[{"role": "user", "content": prompt}],
        )
        # response = openai.ChatCompletion.create(
        #     model="gpt-3.5-turbo",
        #     messages=[{"role": "user", "content": prompt}],
        #     temperature=0.3,
        #     max_tokens=300
        # )
        return response.choices[0].message.content

    def query(self, question, k=3):
        """Complete RAG pipeline"""
        # 1. Retrieve
        chunks = self.retrieve(question, k)

        # 2. Augment
        prompt = self.augment(chunks, question)

        # 3. Generate
        answer = self.generate(prompt)

        return {"answer": answer, "sources": chunks}


# Usage
rag = SimpleRAG()
rag.setup()

# Add documents
rag.add_documents(
    [
        "Python is a programming language created in 1991.",
        "RAG combines retrieval and generation.",
        "Machine learning uses algorithms to learn from data.",
    ]
)

# Query
result = rag.query("What is Python?")
print(result["answer"])
print("\nSources:", result["sources"])
