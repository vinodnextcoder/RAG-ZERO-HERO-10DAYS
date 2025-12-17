import os
import sys
import json
import numpy as np
from typing import List, Dict
from openai import OpenAI
from sentence_transformers import SentenceTransformer
from dotenv import load_dotenv

load_dotenv()

# ===============================
# 🔐 API KEY SETUP
# ===============================
api_key = os.getenv("OPENROUTER_API_KEY")

if not api_key:
    print("❌ ERROR: OPENROUTER_API_KEY not found.")
    sys.exit(1)

client = OpenAI(
    base_url="https://openrouter.ai/api/v1",
    api_key=api_key
)

# ===============================
# 📄 DOCUMENT LOADER
# ===============================
class DocumentLoader:
    """Load documents from various sources"""

    def load_text_file(self, filepath: str) -> str:
        try:
            print(f"[DocumentLoader] Loading TXT: {filepath}")
            with open(filepath, "r", encoding="utf-8") as f:
                return f.read()
        except Exception as e:
            print(f"[ERROR][TXT] {e}")
            return ""

    def load_pdf(self, filepath: str) -> str:
        try:
            print(f"[DocumentLoader] Loading PDF: {filepath}")
            import pypdf
            text = ""

            with open(filepath, "rb") as f:
                reader = pypdf.PdfReader(f)
                for i, page in enumerate(reader.pages):
                    page_text = page.extract_text()
                    if page_text:
                        print(f"[PDF] Extracted page {i+1}")
                        text += page_text + "\n"

            return text
        except Exception as e:
            print(f"[ERROR][PDF] {e}")
            return ""

# ===============================
# ✂️ TEXT CHUNKER
# ===============================
class TextChunker:
    def __init__(self, chunk_size: int = 500, overlap: int = 50):
        self.chunk_size = chunk_size
        self.overlap = overlap

    def chunk_text(self, text: str, source: str) -> List[Dict]:
        print("\n[Chunker] Starting chunking")
        words = text.split()
        print(f"[Chunker] Total words: {len(words)}")

        step = self.chunk_size - self.overlap
        chunks = []

        for i in range(0, len(words), step):
            chunk_words = words[i:i + self.chunk_size]

            chunk = {
                "text": " ".join(chunk_words),
                "source": source,
                "chunk_id": len(chunks) + 1,
                "word_count": len(chunk_words)
            }

            print(f"[Chunker] Created chunk {chunk['chunk_id']} | words: {chunk['word_count']}")
            chunks.append(chunk)

        print(f"[Chunker] Total chunks created: {len(chunks)}\n")
        return chunks

# ===============================
# 🧠 EMBEDDING GENERATOR (FIXED)
# ===============================
class EmbeddingGenerator:
    def __init__(self):
        print("[EmbeddingGenerator] Loading embedding model")
        self.model = SentenceTransformer("all-MiniLM-L6-v2")

    def generate(self, text: str) -> List[float]:
        print("[EmbeddingGenerator] Generating query embedding")
        embedding = self.model.encode(
            text.replace("\n", " ").strip(),
            convert_to_numpy=True
        )
        print(f"[EmbeddingGenerator] Query embedding shape: {embedding.shape}")
        return embedding.tolist()   # 🔥 1D vector

    def generate_batch(self, texts: List[str]) -> List[List[float]]:
        print(f"[EmbeddingGenerator] Generating embeddings for {len(texts)} chunks")
        embeddings = self.model.encode(
            [t.replace("\n", " ").strip() for t in texts],
            convert_to_numpy=True
        )
        print(f"[EmbeddingGenerator] Batch embedding shape: {embeddings.shape}")
        return embeddings.tolist()

# ===============================
# 📦 VECTOR STORE
# ===============================
class VectorStore:
    def __init__(self):
        self.embeddings = []
        self.chunks = []

    def add(self, embeddings: List[List[float]], chunks: List[Dict]):
        print(f"[VectorStore] Adding {len(embeddings)} vectors")
        self.embeddings.extend(embeddings)
        self.chunks.extend(chunks)

    def search(self, query_embedding: List[float], k: int = 3) -> List[Dict]:
        print("[VectorStore] Searching similar vectors")

        if not self.embeddings:
            print("[VectorStore] No embeddings found")
            return []

        query_vec = np.array(query_embedding)
        similarities = []

        for i, emb in enumerate(self.embeddings):
            emb_vec = np.array(emb)
            score = np.dot(query_vec, emb_vec) / (
                np.linalg.norm(query_vec) * np.linalg.norm(emb_vec)
            )
            similarities.append(score)

            print(f"[VectorStore] Similarity with chunk {i+1}: {score:.4f}")

        top_k = np.argsort(similarities)[::-1][:k]

        return [{
            "chunk": self.chunks[i],
            "similarity": float(similarities[i])
        } for i in top_k]

# ===============================
# 🔗 RAG SYSTEM
# ===============================
class RAGSystem:
    def __init__(self):
        self.loader = DocumentLoader()
        self.chunker = TextChunker()
        self.embedder = EmbeddingGenerator()
        self.vector_store = VectorStore()

    def index_document(self, filepath: str):
        print(f"\n[RAG] Indexing document: {filepath}")

        if filepath.endswith(".txt"):
            text = self.loader.load_text_file(filepath)
        elif filepath.endswith(".pdf"):
            text = self.loader.load_pdf(filepath)
        else:
            raise ValueError("Unsupported file format")

        if not text.strip():
            raise ValueError("Document is empty")

        chunks = self.chunker.chunk_text(text, filepath)
        embeddings = self.embedder.generate_batch([c["text"] for c in chunks])
        self.vector_store.add(embeddings, chunks)

        print(f"[RAG] Indexing completed: {len(chunks)} chunks\n")

    def query(self, question: str, k: int = 3) -> Dict:
        print(f"\n[RAG] Query: {question}")

        query_embedding = self.embedder.generate(question)
        results = self.vector_store.search(query_embedding, k)

        if not results:
            return {"answer": "No relevant documents found"}

        context = "\n\n".join(
            f"[Source: {r['chunk']['source']}]\n{r['chunk']['text']}"
            for r in results
        )

        prompt = f"""
        Answer using ONLY the context below.

        Context:
        {context}

        Question: {question}
        """

        response = client.chat.completions.create(
            model="openai/gpt-oss-20b:free",
            messages=[{"role": "user", "content": prompt}]
        )

        return {
            "answer": response.choices[0].message.content,
            "sources": results
        }

# ===============================
# ▶️ USAGE
# ===============================
rag = RAGSystem()
rag.index_document("Sample.pdf")

result = rag.query("What is the main topic?")
print("\n===== FINAL ANSWER =====")
print(result["answer"])
