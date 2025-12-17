import os
import openai
import json
import numpy as np
from typing import List, Dict, Optional

class DocumentLoader:
    """Load documents from various sources"""

    def load_text_file(self, filepath: str) -> str:
        """Load text from .txt file"""
        try:
            with open(filepath, "r", encoding="utf-8") as f:
                return f.read()
        except Exception as e:
            print(f"[DocumentLoader][TXT] Failed to load file '{filepath}': {e}")
            return ""

    def load_pdf(self, filepath: str) -> str:
        """Load text from PDF"""
        try:
            import pypdf
            text = ""

            with open(filepath, "rb") as f:
                reader = pypdf.PdfReader(f)

                for page in reader.pages:
                    page_text = page.extract_text()
                    if page_text:
                        text += page_text + "\n"

            return text

        except Exception as e:
            print(f"[DocumentLoader][PDF] Failed to load file '{filepath}': {e}")
            return ""


class RAGSystem:
    """RAG system: loads and prepares documents for indexing"""

    def __init__(self):
        self.loader = DocumentLoader()

    def index_document(self, filepath: str):
        """Load a document and prepare it for RAG indexing"""
        print(f"[RAG] Starting document indexing")
        print(f"[RAG] File path: {filepath}")

        # Load document
        if filepath.endswith(".txt"):
            print("[RAG] Detected TXT file")
            text = self.loader.load_text_file(filepath)

        elif filepath.endswith(".pdf"):
            print("[RAG] Detected PDF file")
            text = self.loader.load_pdf(filepath)

        else:
            raise ValueError(f"[RAG] Unsupported file type: {filepath}")

        # Validate loaded content
        if not text or not text.strip():
            raise ValueError("[RAG] Loaded document is empty")

        print(f"[RAG] Document loaded successfully")
        print(f"[RAG] Document length: {len(text)} characters")

        return text


# Usage
rag = RAGSystem()
doc_text = rag.index_document("Sample.pdf")

