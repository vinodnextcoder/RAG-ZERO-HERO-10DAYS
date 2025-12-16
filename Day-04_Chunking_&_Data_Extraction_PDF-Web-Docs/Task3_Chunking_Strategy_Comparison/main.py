from pypdf import PdfReader
from dotenv import load_dotenv
import re

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
    def chunking_by_word(self):
        # Tokenize by words
        content = " ".join(self.text_data).split()
        # print(content)

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
            start += (chunk_size - overlap_size)
        print(chunk_words)
        return chunk_text
    
    def chunking_by_sentence(self):
        # Join text data
        content = " ".join(self.text_data)
        # print('=======>>>>>',self.text_data)
        content = content.replace("\n", " ").strip()

        # Split into sentences
        sentences = re.split(r'(?<=[.!?])\s+', content)

        max_words = 100           # similar to chunk_size
        overlap_sentences = 1     # sentence-level overlap

        chunks = []
        current_chunk = []
        current_word_count = 0

        chunk_id = 0
        start_word_pos = 0

        for sentence in sentences:
            sentence_words = sentence.split()
            sentence_word_count = len(sentence_words)

            # If adding sentence exceeds limit → close chunk
            if current_word_count + sentence_word_count > max_words:
                chunk_text = " ".join(current_chunk)

                chunks.append({
                    "chunk_id": chunk_id,
                    "text": chunk_text,
                    "start_pos": start_word_pos,
                    "end_pos": start_word_pos + current_word_count,
                    "word_count": current_word_count
                })

                chunk_id += 1

                # Sentence-level overlap
                current_chunk = current_chunk[-overlap_sentences:] if overlap_sentences else []
                current_word_count = sum(len(s.split()) for s in current_chunk)
                start_word_pos += current_word_count

            # Add sentence
            current_chunk.append(sentence)
            current_word_count += sentence_word_count

        # Add last chunk
        if current_chunk:
            chunk_text = " ".join(current_chunk)
            chunks.append({
                "chunk_id": chunk_id,
                "text": chunk_text,
                "start_pos": start_word_pos,
                "end_pos": start_word_pos + current_word_count,
                "word_count": current_word_count
            })
        # print(chunks)
        return chunks
    
    def chunking_by_paragraph(self):
            """
            Splits text into paragraphs with strong boundary rules.
            Returns a list of dictionaries with 'chunk_id', 'text', 'start_pos', 'end_pos', 'word_count'.
            """
            # Join all text into a single string
            content = " ".join(self.text_data)
            # Remove newline characters that are within sentences
            clean_text = re.sub(r"(?<=\w)\n(?=\w)", " ", content)
            lines = clean_text.split("\n")

            paragraphs = []
            buffer = ""
            chunk_id = 0
            start_pos = 0  # Word-level start position

            for line in lines:
                line = line.strip()
                if not line:
                    continue

                # Paragraph boundary rules
                if buffer and (
                    (line[0].isupper() and buffer.endswith(".")) or re.match(r"^(\d+\.|•|-)", line)
                ):
                    words = buffer.split()
                    end_pos = start_pos + len(words)

                    paragraphs.append({
                        "chunk_id": chunk_id,
                        "text": buffer.strip(),
                        "start_pos": start_pos,
                        "end_pos": end_pos,
                        "word_count": len(words)
                    })

                    chunk_id += 1
                    start_pos = end_pos
                    buffer = line
                else:
                    buffer += " " + line

            # Append last paragraph
            if buffer:
                words = buffer.split()
                end_pos = start_pos + len(words)
                paragraphs.append({
                    "chunk_id": chunk_id,
                    "text": buffer.strip(),
                    "start_pos": start_pos,
                    "end_pos": end_pos,
                    "word_count": len(words)
                })
            print(paragraphs)

            return paragraphs

        

readPdf = ChunkingStrategyComparison("Sample.pdf")
readPdf.add_context()
readPdf.chunking_by_word()
# readPdf.chunking_by_sentence()
# readPdf.chunking_by_paragraph()