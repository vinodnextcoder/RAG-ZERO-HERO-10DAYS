import os,re,sys
from pypdf import PdfReader
from dotenv import load_dotenv
from openai import OpenAI
from sentence_transformers import SentenceTransformer
import numpy as np
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

client = OpenAI(
  base_url="https://openrouter.ai/api/v1",
  api_key=api_key
)


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
        # print('---------------',content)
        self.content = content

    def get_embedding(self):
        """
        Generate embeddings for text (single or batch) using SentenceTransformer
        """

        if not self.content:
            raise ValueError("No content to embed")

        # Load model once (ideally move to __init__ in production)
        model = SentenceTransformer("all-MiniLM-L6-v2")

        # ---- Handle single text or list of texts ----
        if isinstance(self.content, str):
            texts = [self.content.replace("\n", " ").strip()]
        elif isinstance(self.content, list):
            texts = [t.replace("\n", " ").strip() for t in self.content if t]
        else:
            raise TypeError("Content must be a string or list of strings")

        try:
            embeddings = model.encode(texts)
        except Exception as e:
            raise RuntimeError(f"Embedding generation failed: {str(e)}")

        results = []

        for idx, emb in enumerate(embeddings):
            emb_list = emb.tolist()
            emb_array = np.array(emb_list)

            metadata = {
                "index": idx,
                "dimension": len(emb_list),
                "preview": emb_list[:5],  # first few values
                "min": float(emb_array.min()),
                "max": float(emb_array.max()),
                "mean": float(emb_array.mean()),
            }

            results.append({
                "text": texts[idx],
                "embedding": emb_list,
                "metadata": metadata
            })

            # ---- Display summary ----
            print(f"\nEmbedding {idx + 1}")
            print(f"Dimension : {metadata['dimension']}")
            print(f"Preview   : {metadata['preview']}")
            print(f"Stats     : min={metadata['min']:.4f}, "
                f"max={metadata['max']:.4f}, "
                f"mean={metadata['mean']:.4f}")

        return results

        # **** code for apid apikey with openai **
        # response = client.embeddings.create(
        #     model="text-embedding-3-small",
        #     input=text
        # )

        # return response.data[0].embedding

        


readPdf = EmbeddingGenerator("sample.pdf")
readPdf.add_context()
readPdf.get_embedding()
