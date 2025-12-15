import os,re,sys
from pypdf import PdfReader
from dotenv import load_dotenv
from openai import OpenAI
from sentence_transformers import SentenceTransformer
import numpy as np
import chromadb
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

# client = OpenAI(
#   base_url="https://openrouter.ai/api/v1",
#   api_key=api_key
# )


load_dotenv()
class ChromaDBDocument:
    def __init__ (self,collection_name):
        self.collection = collection_name
        print(f"Chromadb initializing")
        self.client = chromadb.Client()

        self.collection = self.client.get_or_create_collection(
            name=collection_name
        )
        print(f"Chromadb initialized with collection: {self.collection}")

        self.content = ""

    def add_context(self):
        # Add documents
        documents = [
            "Python is a high-level programming language",
            "Dogs are loyal and friendly animals",
            "Machine learning is a subset of AI"
        ]

        ids = ["doc1", "doc2", "doc3"]
        metadatas = [
            {"source": "python_book", "page": 1},
            {"source": "animal_guide", "page": 5},
            {"source": "ai_textbook", "page": 10}
        ]

        self.collection.add(
                documents=documents,
                ids=ids,
                metadatas=metadatas
            )

    def search(self):
        # Query for similar documents
        results = self.collection.query(
            query_texts=["programming languages"],
            n_results=2
        )

        print("Similar documents:")
        for i, doc in enumerate(results['documents'][0]):
            print(f"{i+1}. {doc}")
            print(f"   Metadata: {results['metadatas'][0][i]}")
        results1 = self.collection.get(ids=["doc1"])

    def get_by_id(self):

        results = self.collection.get(ids=["doc1","doc2"])
        for doc_id, doc_text, metadata in zip(
            results["ids"], results["documents"], results["metadatas"]
        ):
            print("ID:", doc_id)
            print("Text:", doc_text)
            print("Metadata:", metadata)
            print("-" * 40)


readPdf = ChromaDBDocument("chromadoclearn")
readPdf.add_context()
readPdf.search()
readPdf.get_by_id()
