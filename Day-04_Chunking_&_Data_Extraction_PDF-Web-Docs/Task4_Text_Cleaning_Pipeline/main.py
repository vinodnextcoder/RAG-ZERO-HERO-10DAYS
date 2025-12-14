from pypdf import PdfReader
from dotenv import load_dotenv
import re

load_dotenv()
class CleaningText:
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

    def clean_text(self):
        content = " ".join(self.text_data)
        before_text = content

        # Remove extra whitespace
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

        self.cleaned_text = content
        print(content)
        return content
        

readPdf = CleaningText("Sample.pdf")
readPdf.add_context()
readPdf.clean_text()
# readPdf.chunking_by_word()
