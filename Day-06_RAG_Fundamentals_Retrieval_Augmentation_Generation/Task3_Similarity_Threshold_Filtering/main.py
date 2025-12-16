from openai import OpenAI
import os, sys
import chromadb
from chromadb.config import Settings
from dotenv import load_dotenv

load_dotenv()


class RefinedRAGWithMerge:
    def __init__(self):
        self.client = chromadb.Client(Settings())
        self.collection = None

        # Read API key
        self.api_key = os.getenv("OPENROUTER_API_KEY")
        if not self.api_key:
            print("❌ ERROR: OPENROUTER_API_KEY not found.")
            sys.exit(1)

        self.client_openai = OpenAI(
            base_url="https://openrouter.ai/api/v1",
            api_key=self.api_key,
        )

    def setup(self, collection_name="rag_refined_merge"):
        """Initialize ChromaDB collection"""
        self.collection = self.client.create_collection(name=collection_name)

    def add_documents(self, texts, ids=None, metadatas=None):
        """Add documents with metadata"""
        if ids is None:
            ids = [f"doc_{i}" for i in range(len(texts))]
        self.collection.add(documents=texts, ids=ids, metadatas=metadatas)
    
    def retrieve_with_threshold(self,query,k, threshold=0.7):
        """Retrieve only chunks above similarity threshold"""
        results = self.collection.query(
                query_texts=[query],
                n_results=k
            )
            
        # Filter by similarity (distance is inverse of similarity)
        # Lower distance = higher similarity
        filtered_docs = []
        filtered_metas = []
            
        for doc, meta, distance in zip(
                results['documents'][0],
                results['metadatas'][0],
                results['distances'][0]
            ):
            similarity = 1 - distance  # Convert distance to similarity
            if similarity >= threshold:
                filtered_docs.append(doc)
                filtered_metas.append(meta)
        
        return filtered_docs, filtered_metas

    def summarize_chunk(self, chunk_text):
        """Summarize a single chunk"""
        prompt = f"Summarize the following text concisely in one line, keeping key facts:\n{chunk_text}"
        response = self.client_openai.chat.completions.create(
            model="openai/gpt-oss-20b:free",
            messages=[{"role": "user", "content": prompt}],
        )
        return response.choices[0].message.content

    def merge_and_refine(self, summaries, question):
        """Merge summaries and generate final answer with inline citations"""
        context_text = "\n\n".join([f"[{i+1}] {s['summary']}" for i, s in enumerate(summaries)])
        sources_text = "\n".join([f"[{i+1}] {s['metadata']}" for i, s in enumerate(summaries)])

        prompt = f"""
            You are an AI assistant. Answer the question using ONLY the context below.
            - Only answer the question asked.
            - Combine information from all summaries.
            - Cite sources inline using [1], [2], etc.
            - Do NOT invent sources outside the context.

            Context:
            {context_text}

            Question:
            {question}

            Answer and then list 'Sources' section:
            {sources_text}
            """
        response = self.client_openai.chat.completions.create(
            model="openai/gpt-oss-20b:free",
            messages=[{"role": "user", "content": prompt}],
        )
        return response.choices[0].message.content

    def query(self, question, k=3):
        """Full RAG pipeline: retrieve → summarize → merge/refine"""
        # chunks = self.retrieve(question, k)
        chunks,metadata = self.retrieve_with_threshold(question,k, 0.1)
        print(chunks, metadata)

        # # Step 1: Summarize each chunk
        summaries = []
        for chunk in chunks:
            summary_text = self.summarize_chunk(chunk)
            summaries.append({"summary": summary_text, "metadata": metadata})

        # # Step 2: Merge summaries and generate final answer
        answer = self.merge_and_refine(summaries, question)
        return {"answer": answer, "sources": chunks}


# ---------------- Usage ----------------
rag = RefinedRAGWithMerge()
rag.setup()

# Add documents
documents = [
    "Semantic search retrieves documents based on meaning, not keywords.",
    "RAG combines retrieval with generation to ground LLM responses.",
    "Embeddings convert text into dense numerical vectors."
]
metadatas = [
    {"source": "nlp_guide.pdf", "page": 5},
    {"source": "rag_intro.md", "section": "overview"},
    {"source": "embeddings_blog.md", "author": "OpenAI"}
]
ids = ["chunk_1", "chunk_2", "chunk_3"]

rag.add_documents(documents, ids, metadatas)

# Query example
query_text = "What is semantic search?"
result = rag.query(query_text, k=3)
print(result)

# print("Answer:\n", result["answer"])
# print("\nSources:")
# for i, chunk in enumerate(result["sources"], 1):
#     print(f"[{i}] {chunk['metadata']}")
