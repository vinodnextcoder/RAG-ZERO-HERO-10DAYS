import os
import sys
import json
import numpy as np
from typing import List, Dict
from openai import OpenAI
from sentence_transformers import SentenceTransformer
from dotenv import load_dotenv
from langchain_community.document_loaders import PyPDFLoader
from langchain_community.document_loaders import TextLoader
from langchain_text_splitters import RecursiveCharacterTextSplitter


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
    def load_text_file(self, filepath: str) -> str:
        try:
            print(f"[DocumentLoader] Loading TXT: {filepath}")
            loader= TextLoader(filepath)
            self.documents = loader.load()
        except Exception as e:
            print(f"[ERROR][TXT] {e}")
            return ""

    def load_pdf(self, filepath: str) -> str:
        try:
            print(f"[DocumentLoader] Loading PDF: {filepath}")
            loader = PyPDFLoader(filepath)
            documents = loader.load()
            return documents
        except Exception as e:
            print(f"[ERROR][PDF] {e}")
            return ""
        
class TextChunker:

    def chunk_text(self,documents) -> any:
        # 2. Split text
        print(documents)
        text_splitter = RecursiveCharacterTextSplitter(
            chunk_size=1000,
            chunk_overlap=200
        )
        chunks = text_splitter.split_documents(documents)
        print(chunks)
        
        return chunks


# ===============================
# 🔗 RAG SYSTEM
# ===============================
class Langchainsystem:
    def __init__(self):
        self.loader = DocumentLoader()
        doc = self.loader.load_pdf("Sample.pdf")
        self.textChunker = TextChunker()
        self.textChunker.chunk_text(doc)

# ===============================
# ▶️ USAGE
# ===============================
if __name__ == "__main__":
    rag = Langchainsystem()
  
