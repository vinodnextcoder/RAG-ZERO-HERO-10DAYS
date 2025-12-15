from dotenv import load_dotenv
import chromadb
from sentence_transformers import SentenceTransformer
from typing import List, Dict, Optional

load_dotenv()

class SemanticSearchEngine:
    def __init__(self, collection_name: str, persist_path: Optional[str] = None):
        """Initialize ChromaDB semantic search engine"""
        print("Initializing ChromaDB...")
        if persist_path:
            self.client = chromadb.Client(
                chromadb.config.Settings(persist_directory=persist_path)
            )
        else:
            self.client = chromadb.Client()

        self.collection = self.client.get_or_create_collection(
            name=collection_name
        )
        self.model = SentenceTransformer("all-MiniLM-L6-v2")
        print(f"ChromaDB ready with collection: {collection_name}")

    # ------------------ Indexing ------------------
    def index_documents(
        self,
        documents: List[str],
        ids: List[str],
        metadatas: Optional[List[Dict]] = None
    ):
        """Add documents to ChromaDB (no hardcoded data)"""
        if not documents or not ids:
            raise ValueError("Documents and IDs are required")

        if len(documents) != len(ids):
            raise ValueError("Documents and IDs length mismatch")

        embeddings = self.model.encode(documents).tolist()

        self.collection.add(
            documents=documents,
            ids=ids,
            embeddings=embeddings,
            metadatas=metadatas
        )
        print(f"Indexed {len(documents)} documents")

    # ------------------ Remove ------------------
    def remove_documents(self, ids: List[str]):
        """Remove documents by IDs"""
        if not ids:
            raise ValueError("IDs required for deletion")

        self.collection.delete(ids=ids)
        print(f"Removed documents: {ids}")

    # ------------------ Semantic Search ------------------
    def semantic_search(
        self,
        query: str,
        top_k: int = 5,
        where: Optional[Dict] = None
    ):
        """Perform semantic search with optional metadata filtering"""
        if not query:
            raise ValueError("Query cannot be empty")

        query_embedding = self.model.encode(query).tolist()

        results = self.collection.query(
            query_embeddings=[query_embedding],
            n_results=top_k,
            where=where,
            include=["documents", "metadatas", "distances"]
        )

        return self._format_results(results)

    # ------------------ Helpers ------------------
    def _format_results(self, results):
        """Format search results with similarity scores"""
        formatted = []
        docs = results.get("documents", [[]])[0]
        metas = results.get("metadatas", [[]])[0]
        distances = results.get("distances", [[]])[0]

        for doc, meta, dist in zip(docs, metas, distances):
            formatted.append({
                "document": doc,
                "metadata": meta,
                "similarity_score": round(1 - dist, 4)
            })

        return formatted


# ------------------ Example Usage ------------------
if __name__ == "__main__":
    engine = SemanticSearchEngine(collection_name="my_semantic_docs")

    # Index documents (dynamic input)
    engine.index_documents(
        documents=[
            "Python is a popular programming language",
            "Dogs are very loyal animals",
            "Artificial Intelligence includes machine learning"
        ],
        ids=["d1", "d2", "d3"],
        metadatas=[
            {"source": "tech", "page": 1},
            {"source": "animals", "page": 5},
            {"source": "ai", "page": 10}
        ]
    )

    # Semantic search
    results = engine.semantic_search(
        query="What is machine learning?",
        top_k=2,
        where={"source": "ai"}
    )

    for i, r in enumerate(results, 1):
        print(f"\nResult {i}")
        print("Score:", r["similarity_score"])
        print("Text:", r["document"])
        print("Metadata:", r["metadata"])
