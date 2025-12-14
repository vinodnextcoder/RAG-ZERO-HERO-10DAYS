import os,re
from pypdf import PdfReader
from dotenv import load_dotenv

load_dotenv()
class EmbeddingGenerator:
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
        print(f"Total pages detected: {total_pages}")
        print("Starting text extraction...\n")
        for page_number in range(start_page - 1, end_page):
            page = reader.pages[page_number]
            content = page.extract_text() or ""
            content = re.sub(r"\s+", " ", content)

            # Normalize line breaks
            content = re.sub(r"(?<=\w)\n(?=\w)", " ", content)
            content = re.sub(r"\r\n|\r", "\n", content)

            # Remove special characters
            content = re.sub(r"[^A-Za-z0-9\s.,;:!?()-]", "", content)

            # Fix encoding issues (simple example)
            content = content.replace("â€“", "-").replace("â€˜", "'").replace("â€™", "'")

            # Normalize quotes and dashes
            content = content.replace("“", '"').replace("”", '"')
            content = content.replace("‘", "'").replace("’", "'")
            content = content.replace("–", "-").replace("—", "-")

        print("\n✅ PDF extraction completed.")
        print('---------------',content)
        


readPdf = EmbeddingGenerator("pdf-sample.pdf")
readPdf.add_context()
