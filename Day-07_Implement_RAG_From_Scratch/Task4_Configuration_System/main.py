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
# ⚙️ CONFIG CLASS
# ===============================
class Config:
    DEFAULTS = {
        "chunk_size": 500,
        "overlap": 50,
        "top_k": 3,
        "similarity_threshold": 0.0,
        "embedding_model": "all-MiniLM-L6-v2",
        "llm": {
            "model": "openai/gpt-oss-20b:free",
            "temperature": 0.0,
            "max_tokens": 512
        }
    }

    def __init__(self, path: str = "config.json"):
        print(f"[Config] Loading config from {path}")
        self.data = json.loads(json.dumps(self.DEFAULTS))  # deep copy

        try:
            with open(path, "r", encoding="utf-8") as f:
                user_cfg = json.load(f)
                self._merge(self.data, user_cfg)
        except FileNotFoundError:
            print("[Config] config.json not found → using defaults")
        except json.JSONDecodeError as e:
            print(f"[Config] Invalid JSON → {e}")
            print("[Config] Using defaults")

        self._validate()
        print("[Config] Config loaded successfully\n")

    def _merge(self, base: dict, override: dict):
        for k, v in override.items():
            if isinstance(v, dict) and k in base:
                self._merge(base[k], v)
            else:
                base[k] = v

    def _validate(self):
        if self.data["chunk_size"] <= 0:
            raise ValueError("chunk_size must be > 0")

        if self.data["overlap"] < 0:
            raise ValueError("overlap cannot be negative")

        if self.data["overlap"] >= self.data["chunk_size"]:
            raise ValueError("overlap must be smaller than chunk_size")

        if self.data["top_k"] <= 0:
            raise ValueError("top_k must be > 0")

        if not (0.0 <= self.data["llm"]["temperature"] <= 1.0):
            raise ValueError("temperature must be between 0 and 1")

        if self.data["llm"]["max_tokens"] <= 0:
            raise ValueError("max_tokens must be > 0")

# ===============================
# 📄 DOCUMENT LOADER
# ===============================
class DocumentLoader:
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
                        print(f"[PDF] Extracted page {i + 1}")
                        text += page_text + "\n"

            return text
        except Exception as e:
            print(f"[ERROR][PDF] {e}")
            return ""

# ===============================
# ✂️ TEXT CHUNKER
# ===============================
class TextChunker:
    def __init__(self, config: Config):
        self.chunk_size = config.data["chunk_size"]
        self.overlap = config.data["overlap"]

    def chunk_text(self, text: str, source: str) -> List[Dict]:
        print("\n[Chunker] Starting chunking")
        words = text.split()
        step = self.chunk_size - self.overlap

        chunks = []
        for i in range(0, len(words), step):
            chunk_words = words[i:i + self.chunk_size]
            chunks.append({
                "text": " ".join(chunk_words),
                "source": source,
                "chunk_id": len(chunks) + 1,
                "word_count": len(chunk_words)
            })

            print(f"[Chunker] Chunk {len(chunks)} | words: {len(chunk_words)}")

        print(f"[Chunker] Total chunks: {len(chunks)}\n")
        return chunks

# ===============================
# 🧠 EMBEDDING GENERATOR
# ===============================
class EmbeddingGenerator:
    def __init__(self, config: Config):
        model_name = config.data["embedding_model"]
        print(f"[EmbeddingGenerator] Loading model: {model_name}")
        self.model = SentenceTransformer(model_name)

    def generate(self, text: str) -> List[float]:
        emb = self.model.encode(
            text.replace("\n", " ").strip(),
            convert_to_numpy=True
        )
        return emb.tolist()

    def generate_batch(self, texts: List[str]) -> List[List[float]]:
        embs = self.model.encode(
            [t.replace("\n", " ").strip() for t in texts],
            convert_to_numpy=True
        )
        return embs.tolist()

# ===============================
# 📦 VECTOR STORE
# ===============================
class VectorStore:
    def __init__(self, similarity_threshold: float):
        self.embeddings = []
        self.chunks = []
        self.similarity_threshold = similarity_threshold

    def add(self, embeddings: List[List[float]], chunks: List[Dict]):
        self.embeddings.extend(embeddings)
        self.chunks.extend(chunks)
        print(f"[VectorStore] Stored {len(embeddings)} vectors")

    def search(self, query_embedding: List[float], k: int) -> List[Dict]:
        if not self.embeddings:
            print("[VectorStore] No vectors found")
            return []

        query_vec = np.array(query_embedding)
        scores = []

        for i, emb in enumerate(self.embeddings):
            emb_vec = np.array(emb)
            score = np.dot(query_vec, emb_vec) / (
                np.linalg.norm(query_vec) * np.linalg.norm(emb_vec)
            )

            if score >= self.similarity_threshold:
                scores.append((i, score))

        scores.sort(key=lambda x: x[1], reverse=True)
        scores = scores[:k]

        return [{
            "chunk": self.chunks[i],
            "similarity": float(score)
        } for i, score in scores]

# ===============================
# 🔗 RAG SYSTEM
# ===============================
class RAGSystem:
    def __init__(self, config_path: str = "config.json"):
        self.config = Config(config_path)

        self.loader = DocumentLoader()
        self.chunker = TextChunker(self.config)
        self.embedder = EmbeddingGenerator(self.config)
        self.vector_store = VectorStore(
            self.config.data["similarity_threshold"]
        )

    def index_document(self, filepath: str):
        print(f"\n[RAG] Indexing: {filepath}")

        if filepath.endswith(".txt"):
            text = self.loader.load_text_file(filepath)
        elif filepath.endswith(".pdf"):
            text = self.loader.load_pdf(filepath)
        else:
            raise ValueError("Unsupported file type")

        if not text.strip():
            raise ValueError("Document is empty")

        chunks = self.chunker.chunk_text(text, filepath)
        embeddings = self.embedder.generate_batch(
            [c["text"] for c in chunks]
        )

        self.vector_store.add(embeddings, chunks)
        print(f"[RAG] Indexed {len(chunks)} chunks\n")

    def query(self, question: str) -> Dict:
        print(f"\n[RAG] Query: {question}")

        query_emb = self.embedder.generate(question)
        k = self.config.data["top_k"]

        results = self.vector_store.search(query_emb, k)

        if not results:
            return {"answer": "No relevant documents found", "sources": []}

        context = "\n\n".join(
            f"[Source: {r['chunk']['source']}]\n{r['chunk']['text']}"
            for r in results
        )

        llm_cfg = self.config.data["llm"]

        response = client.chat.completions.create(
            model=llm_cfg["model"],
            temperature=llm_cfg["temperature"],
            max_tokens=llm_cfg["max_tokens"],
            messages=[{
                "role": "user",
                "content": f"""
Answer using ONLY the context below.

Context:
{context}

Question: {question}
"""
            }]
        )

        return {
            "answer": response.choices[0].message.content,
            "sources": results
        }

# ===============================
# ▶️ USAGE
# ===============================
if __name__ == "__main__":
    rag = RAGSystem("config.json")
    rag.index_document("Sample.pdf")

    result = rag.query("What is the main topic?")
    print("\n===== FINAL ANSWER =====")
    print(result["answer"])
