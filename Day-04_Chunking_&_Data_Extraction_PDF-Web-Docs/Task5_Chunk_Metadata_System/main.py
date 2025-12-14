# task5_chunk_metadata.py
import os
import json
from datetime import datetime
from pypdf import PdfReader
from dotenv import load_dotenv

load_dotenv()


class Chunk:
    def __init__(self, file_path):
        self.file_path = file_path
        self.chunks = []
        self.chunk_size = 500  # characters per chunk
        self.chunk_overlap = 50  # overlapping characters
        print(f"DocumentManager initialized with file: {self.file_path}")

    def add_context(self):
        print("Loading document...")
        reader = PdfReader(self.file_path)

        if reader.is_encrypted:
            raise Exception("PDF is password-protected and cannot be read.")

        total_pages = len(reader.pages)
        print(f"Total pages detected: {total_pages}")

        chunk_id = 1

        for page_number, page in enumerate(reader.pages, start=1):
            page_text = page.extract_text() or ""
            text_length = len(page_text)
            start = 0
            chunk_index = 1

            while start < text_length:
                end = min(start + self.chunk_size, text_length)
                chunk_text = page_text[start:end]

                # Add chunk metadata
                chunk = {
                    "chunk_id": chunk_id,
                    "source": os.path.basename(self.file_path),
                    "page_number": page_number,
                    "chunk_index": chunk_index,
                    "start_char": start,
                    "end_char": end,
                    "word_count": len(chunk_text.split()),
                    "char_count": len(chunk_text),
                    "timestamp": datetime.now().isoformat(),
                    "preview": chunk_text[:50],
                    "text": chunk_text,
                }

                self.chunks.append(chunk)
                chunk_id += 1
                chunk_index += 1
                start += self.chunk_size - self.chunk_overlap

        print(f"\n✅ PDF processed into {len(self.chunks)} chunks.")

    # Export all chunks to JSON
    def export_chunks_to_json(self, output_file="chunks.json"):
        with open(output_file, "w", encoding="utf-8") as f:
            json.dump(self.chunks, f, ensure_ascii=False, indent=4)
        print(f"Chunks exported to {output_file}")

    # Filter chunks by metadata
    def filter_chunks(self, min_words=None, max_words=None, page_number=None):
        results = self.chunks
        if min_words is not None:
            results = [c for c in results if c["word_count"] >= min_words]
        if max_words is not None:
            results = [c for c in results if c["word_count"] <= max_words]
        if page_number is not None:
            results = [c for c in results if c["page_number"] == page_number]
        return results

    # Get statistics of chunks
    def get_chunk_statistics(self):
        total_chunks = len(self.chunks)
        total_words = sum(c["word_count"] for c in self.chunks)
        total_chars = sum(c["char_count"] for c in self.chunks)
        avg_words = total_words / total_chunks if total_chunks else 0
        avg_chars = total_chars / total_chunks if total_chunks else 0

        return {
            "total_chunks": total_chunks,
            "total_words": total_words,
            "total_chars": total_chars,
            "average_words_per_chunk": avg_words,
            "average_chars_per_chunk": avg_chars,
        }
    

chunk_info = Chunk("Sample.pdf")
chunk_info.add_context()
chunk_info.export_chunks_to_json()

stats = chunk_info.get_chunk_statistics()
print("\n📊 Chunk Statistics:", stats)

# Example: Filter chunks with more than 50 words
filtered = chunk_info.filter_chunks(min_words=50)
print(f"\nFiltered chunks (>=50 words): {len(filtered)}")

