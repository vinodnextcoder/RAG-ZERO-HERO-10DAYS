from pypdf import PdfReader
from dotenv import load_dotenv

load_dotenv()
class ChunkingStrategyComparison:
    def __init__ (self,file_path):
        self.file_path = file_path
        print(f"DocumentManager initialized with file: {self.file_path}")
        self.content = ""

    def add_context(self):
        print("Loading document...")
        print(f"File path: {self.file_path}")

        reader = PdfReader(self.file_path)

        if reader.is_encrypted:
            raise Exception("PDF is password-protected and cannot be read.")

        total_pages = len(reader.pages)
        start_page = 1
        end_page = total_pages

        text_per_page = []
        page_data = []


        print(f"Total pages detected: {total_pages}")
        print("Starting text extraction...\n")

        for page_number in range(start_page - 1, end_page):
            page = reader.pages[page_number]
            page_text = page.extract_text() or ""
            text_per_page.append(page_text)
            page_details = {
                "page_num": page_number + 1,
                "content": page_text
            }
            page_data.append(page_details)
            # 🔹 Progress indicator
            progress = ((page_number + 1) / total_pages) * 100
            print(
                f"📄 Processing page {page_number + 1}/{total_pages} "
                f"({progress:.2f}%)",
                end="\r"
            )
        self.text_data = text_per_page

        print("\n✅ PDF extraction completed.")
    def chunking(self):
            # Join and tokenize
            content = " ".join(self.text_data).split()
            word_length = len(content)

            chunk_size = 10
            overlap_size = 3

            start = 0
            chunk_id = 0
            chunk_text = []

            while start < word_length:
                end = min(start + chunk_size, word_length)
                chunk_words = content[start:end]

                chunk_text.append({
                    "chunk_id": chunk_id,
                    "text": " ".join(chunk_words),
                    "start_pos": start,
                    "end_pos": end,
                    "word_count": len(chunk_words)
                })

                chunk_id += 1

                # Move start with overlap
                start += (chunk_size - overlap_size)
            print(chunk_text)

            return chunk_text



readPdf = ChunkingStrategyComparison("Sample.pdf")
readPdf.add_context()
readPdf.chunking()