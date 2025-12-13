import os
import sys
from pypdf import PdfReader
from dotenv import load_dotenv

load_dotenv()
class DocPdfReader:
    def __init__ (self,file_path):

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

        self.file_path = file_path
        print(f"DocumentManager initialized with file: {self.file_path}")
        self.content = ""

    def add_context(self):
        print("Loading document...")
        print(f"File path: {self.file_path}")
        reader = PdfReader(self.file_path)
        if reader.is_encrypted:
            raise "PDF is password-protected and cannot be read."

        total_pages = len(reader.pages)
        number_of_pages = len(reader.pages)
        start_page=1
        end_page=number_of_pages
        text_per_page = []
        page_data = []
        text_per_page = []
        page_data = []

        # Ensure start_page and end_page are within the valid range of the PDF
        for page_number in range(start_page - 1, end_page):
            page = reader.pages[page_number]
            page_text = page.extract_text() or ""

            # Store plain text in a list
            text_per_page.append(page_text)

            # Corrected dictionary syntax: Use a colon (:) instead of (=)
            # and provide a key for the page number.
            page_details = {
                "page_num": page_number + 1,  # Adding 1 to make it 1-indexed for readability
                "content": page_text
            }
            # Append the dictionary to your page_data list
            page_data.append(page_details)

        metadata = reader.metadata or {}

        result = {
            "file": os.path.basename(self.file_path),
            "total_pages": total_pages,
            "extracted_pages": end_page - start_page + 1,
            "page_range": (start_page, end_page),
            "text_per_page": page_data,
            "total_page_data":text_per_page,
            "metadata": {
                "title": metadata.get("/Title"),
                "author": metadata.get("/Author"),
                "creator": metadata.get("/Creator"),
                "producer": metadata.get("/Producer"),
            },
        }

        print(result)


readPdf = DocPdfReader("Sample.pdf")
readPdf.add_context()
