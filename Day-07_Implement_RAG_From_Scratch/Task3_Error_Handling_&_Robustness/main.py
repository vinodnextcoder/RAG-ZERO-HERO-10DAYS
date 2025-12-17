import os
import sys
import json
import time
import numpy as np
from typing import List, Dict
from openai import OpenAI
from sentence_transformers import SentenceTransformer
from dotenv import load_dotenv
from requests.exceptions import RequestException

load_dotenv()

# ===============================
# 🔐 API KEY SETUP
# ===============================
api_key = os.getenv("OPENROUTER_API_KEY")

if not api_key:
    print("[ERROR] OPENROUTER_API_KEY not found. Set it in environment variables.")
    sys.exit(1)

try:
    client = OpenAI(
        base_url="https://openrouter.ai/api/v1",
        api_key=api_key
    )
    print("[INFO] OpenRouter client initialized")
except Exception as e:
    print(f"[ERROR] Failed to initialize OpenAI client: {e}")
    sys.exit(1)

# ===============================
# 📄 DOCUMENT LOADER
# ===============================
class DocumentLoader:
    """Load documents from various sources"""

    def load_text_file(self, filepath: str) -> str:
        if not os.path.exists(filepath):
            print(f"[ERROR] File not found: {filepath}")
            return ""
        try:
            print(f"[INFO] Loading TXT file: {filepath}")
            with open(filepath, "r", encoding="utf-8") as f:
                return f.read()
        except Exception as e:
            print(f"[ERROR] TXT read failed: {e}")
            return ""

    def load_pdf(self, filepath: str) -> str:
        if not os.path.exists(filepath):
            print(f"[ERROR] File not found: {filepath}")
            return ""
        try:
            print(f"[INFO] Loading PDF file: {filepath}")
            import pypdf
            text = ""
            with open(filepath, "rb") as f:
                reader = pypdf.PdfReader(f)
                for i, page in enumerate(reader.pages):
                    page_text = page.extract_text()
                    if page_text:
                        text += page_text + "\n"
            return text
        except Exception as e:
            print(f"[ERROR] PDF read failed: {e}")
            return ""

# ===============================
# ✂️ TEXT CHUNKER
# ===============================
class TextChunker:
    def __init__(self, chunk_size: int = 500, overlap: int = 50):
        self.chunk_size = chunk_size
        self.overlap = overlap

    def chunk_text(self, text: str, source: str) -> List[Dict]:
        if not text.strip():
            print("[WARN] Empty text received for chunking")
            return []

        words = text.split()
        step = max(1, self.chunk_size - self.overlap)
        chunks = []

        for i in range(0, len(words), step):
            chunk_words = words[i:i + self.chunk_size]
            chunks.append({
                "text": " ".join(chunk_words),
                "source": source,
                "chunk_id": len(chunks) + 1,
                "word_count": len(chunk_words)
            })

        print(f"[INFO] Created {len(chunks)} chunks")
        return chunks

# ===============================
# 🧠 EMBEDDING GENERATOR
# ===============================
class EmbeddingGenerator:
    def __init__(self):
        try:
            print("[INFO] Loading embedding model")
            self.model = SentenceTransformer("all-MiniLM-L6-v2")
        except Exception as e:
            print(f"[ERROR] Failed to load embedding model: {e}")
            raise

    def generate(self, text: str) -> List[float]:
        if not text.strip():
            raise ValueError("Cannot generate embedding for empty text")
        return self.model.encode(text, convert_to_numpy=True).tolist()

    def generate_batch(self, texts: List[str]) -> List[List[float]]:
        if not texts:
            print("[WARN] No texts provided for batch embedding")
            return []
        return self.model.encode(texts, convert_to_numpy=True).tolist()

# ===============================
# 📦 VECTOR STORE
# ===============================
class VectorStore:
    def __init__(self):
        self.embeddings = []
        self.chunks = []

    def add(self, embeddings: List[List[float]], chunks: List[Dict]):
        if not embeddings or not chunks:
            print("[WARN] Nothing to add to vector store")
            return
        self.embeddings.extend(embeddings)
        self.chunks.extend(chunks)
        print(f"[INFO] Vector store size: {len(self.embeddings)}")

    def search(self, query_embedding: List[float], k: int = 3) -> List[Dict]:
        if not self.embeddings:
            print("[WARN] Vector store is empty")
            return []

        query_vec = np.array(query_embedding)
        similarities = []

        for emb in self.embeddings:
            emb_vec = np.array(emb)
            score = float(np.dot(query_vec, emb_vec) / (
                np.linalg.norm(query_vec) * np.linalg.norm(emb_vec)
            ))
            similarities.append(score)

        top_k = np.argsort(similarities)[::-1][:k]
        return [
            {"chunk": self.chunks[i], "similarity": similarities[i]}
            for i in top_k
        ]

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
        print(f"[INFO] Indexing document: {filepath}")

        if not isinstance(filepath, str):
            raise TypeError("Filepath must be a string")

        if filepath.endswith(".txt"):
            text = self.loader.load_text_file(filepath)
        elif filepath.endswith(".pdf"):
            text = self.loader.load_pdf(filepath)
        else:
            raise ValueError("Unsupported file format")

        if not text.strip():
            raise ValueError("Document is empty or unreadable")

        chunks = self.chunker.chunk_text(text, filepath)
        embeddings = self.embedder.generate_batch([c["text"] for c in chunks])
        self.vector_store.add(embeddings, chunks)

    def query(self, question: str, k: int = 3) -> Dict:
        if not question.strip():
            return {"error": "Question cannot be empty"}

        try:
            query_embedding = self.embedder.generate(question)
            results = self.vector_store.search(query_embedding, k)

            if not results:
                return {"answer": "No relevant documents found", "sources": []}

            context = "\n\n".join(r["chunk"]["text"] for r in results)

            prompt = (
                "Answer ONLY from the context below.\n\n"
                f"Context:\n{context}\n\n"
                f"Question: {question}"
            )

            response = client.chat.completions.create(
                model="openai/gpt-oss-20b:free",
                messages=[{"role": "user", "content": prompt}],
                timeout=30
            )

            return {
                "answer": response.choices[0].message.content,
                "sources": results
            }

        except RequestException:
            return {"error": "Network error. Please try again later."}
        except Exception as e:
            print(f"[ERROR] Query failed: {e}")
            return {"error": "Unexpected error during query"}

# ===============================
# ▶️ USAGE
# ===============================
if __name__ == "__main__":
    try:
        rag = RAGSystem()
        rag.index_document("Sample.pdf")
        result = rag.query("What is the main topic?")
        print("\n===== FINAL RESULT =====")
        print(json.dumps(result, indent=2))
    except Exception as e:
        print(f"[FATAL] {e}")