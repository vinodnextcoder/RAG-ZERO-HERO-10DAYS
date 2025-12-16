from openai import OpenAI
import os, sys
import chromadb
from chromadb.config import Settings
from dotenv import load_dotenv

load_dotenv()


class MultiQueryRAG:
    def __init__(self):
        # ---------------- ChromaDB ----------------
        self.chroma_client = chromadb.Client(Settings())
        self.collection = None

        # ---------------- OpenRouter / LLM ----------------
        api_key = os.getenv("OPENROUTER_API_KEY")
        if not api_key:
            print("❌ ERROR: OPENROUTER_API_KEY not found")
            sys.exit(1)

        self.llm = OpenAI(
            base_url="https://openrouter.ai/api/v1",
            api_key=api_key,
        )

    # ---------------- Setup ----------------

    def setup(self, collection_name="multi_query_rag"):
        self.collection = self.chroma_client.create_collection(
            name=collection_name
        )

    def add_documents(self, documents, ids=None, metadatas=None):
        if ids is None:
            ids = [f"doc_{i}" for i in range(len(documents))]

        self.collection.add(
            documents=documents,
            ids=ids,
            metadatas=metadatas
        )

    # ---------------- Multi-Query Generation ----------------

    def generate_queries(self, question, n=4):
        """
        LLM rewrites user question into multiple semantic variants
        """
        prompt = f"""
Generate {n} different search queries for the question below.
- Same meaning
- Different wording
- Short and clear

Question:
{question}

Return one query per line.
"""

        response = self.llm.chat.completions.create(
            model="openai/gpt-oss-20b:free",
            messages=[{"role": "user", "content": prompt}],
        )

        queries = response.choices[0].message.content.split("\n")
        return [q.strip("- ").strip() for q in queries if q.strip()]

    # ---------------- Retrieval ----------------

    def retrieve_documents(self, queries, k=3):
        """
        Retrieve documents for each query and deduplicate results
        """
        doc_map = {}

        for query in queries:
            results = self.collection.query(
                query_texts=[query],
                n_results=k
            )

            for doc, meta in zip(
                results["documents"][0],
                results["metadatas"][0]
            ):
                doc_map[doc] = meta  # dedupe by content

        return list(doc_map.keys()), list(doc_map.values())

    # ---------------- Answer Generation ----------------

    def generate_answer(self, question, documents):
        """
        Answer using BOTH:
        - documents as factual source
        - LLM for reasoning & clarity
        """
        context = "\n\n".join(documents)

        prompt = f"""
You are an AI assistant answering a question using retrieved documents.

Rules:
1. The documents are the PRIMARY source of facts.
2. You MAY use your general knowledge ONLY to:
   - connect ideas
   - explain clearly
   - rephrase or summarize
3. DO NOT add new facts not supported by the documents.
4. If the documents are insufficient, say:
   "The answer is not fully available in the provided documents."

Documents:
{context}

Question:
{question}

Answer:
- Be concise
- Answer ONLY what is asked
"""

        response = self.llm.chat.completions.create(
            model="openai/gpt-oss-20b:free",
            messages=[{"role": "user", "content": prompt}],
        )

        return response.choices[0].message.content

    # ---------------- Full Pipeline ----------------

    def query(self, question, k=3):
        queries = self.generate_queries(question)
        documents, metadatas = self.retrieve_documents(queries, k)
        answer = self.generate_answer(question, documents)

        return {
            "question": question,
            "generated_queries": queries,
            "answer": answer,
            "sources": metadatas
        }


# ---------------- Example Usage ----------------

rag = MultiQueryRAG()
rag.setup()

documents = [
    "Semantic search retrieves documents based on meaning rather than keywords.",
    "RAG combines document retrieval with text generation to ground LLM responses.",
    "Embeddings convert text into dense numerical vectors for similarity search."
]

metadatas = [
    {"source": "nlp_guide.pdf"},
    {"source": "rag_intro.md"},
    {"source": "embeddings_blog.md"}
]

rag.add_documents(documents, metadatas=metadatas)

result = rag.query("What is semantic search?", k=2)

print("\nGenerated Queries:")
for q in result["generated_queries"]:
    print("-", q)

print("\nAnswer:")
print(result["answer"])

print("\nSources:")
for s in result["sources"]:
    print(s)
