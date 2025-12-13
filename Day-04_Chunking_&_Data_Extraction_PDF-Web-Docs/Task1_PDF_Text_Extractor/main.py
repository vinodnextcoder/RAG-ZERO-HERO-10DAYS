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
        number_of_pages = len(reader.pages)
        page = reader.pages[0]
        text = page.extract_text()
        print('::::::::',page)



readPdf = DocPdfReader("Sample.pdf")
readPdf.add_context()

