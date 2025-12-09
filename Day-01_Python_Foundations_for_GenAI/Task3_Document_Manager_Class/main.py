import json
class DocumentManager:
    def __init__ (self,file_path):
        self.file_path = file_path
        print(f"DocumentManager initialized with file: {self.file_path}")
        self.content = ""

    def load_document(self):
        print("Loading document...")
        print(f"File path: {self.file_path}")
        try:
            with open(self.file_path, 'r', encoding='utf-8') as file:
                self.content = file.read()
                print("Document Content:")
                print(self.content)
        except FileNotFoundError:
            print(f"The file at {self.file_path} does not exist.")
        except Exception as e:
            print(f"An error occurred: {e}")

    def search_documents(self,keyword):
        print(f"Searching for keyword: {keyword}")
        if keyword in self.content:
            print(f"Keyword '{keyword}' found in document.")
        else:
            print(f"Keyword '{keyword}' not found in document.")


    def calculate_document_statistics(self):
        content = self.content
        line_count = 0
        total_word_count = 0
        total_char_count = 0
        total_sentence_dot = 0
        total_sentence_exclamation = 0
        total_sentence_question = 0

        for line in content.split("\n"):
            line_count += 1

            # character count
            total_char_count += len(line)

            # word count
            words = line.split()
            total_word_count += len(words)

            # sentence counts
            total_sentence_dot += line.count(".")
            total_sentence_exclamation += line.count("!")
            total_sentence_question += line.count("?")

            print(f"Line {line_count} has {len(words)} words.")

        total_sentences = (
            total_sentence_dot +
            total_sentence_exclamation +
            total_sentence_question
        )

        # 🔹 PRINT STATEMENTS (as requested)
        print("\nDocument Statistics:")
        print(f"Total Lines: {line_count}")
        print(f"Total Words: {total_word_count}")
        print(f"Total Characters: {total_char_count}")
        print(f"Total Sentences (by '.'): {total_sentence_dot}")
        print(f"Total Sentences (by '!'): {total_sentence_exclamation}")
        print(f"Total Sentences (by '?'): {total_sentence_question}")
        print(f"Total Sentences: {total_sentences}")

        # 🔹 JSON / DICT RESULT
        result = {
            "total_lines": line_count,
            "total_words": total_word_count,
            "total_characters": total_char_count,
            "total_sentences_by_dot": total_sentence_dot,
            "total_sentences_by_exclamation": total_sentence_exclamation,
            "total_sentences_by_question": total_sentence_question,
            "total_sentences": total_sentences
        }

        return result
    
def export_to_json(data,output_file):
    """
    Export document statistics to a JSON file
    """
    # Get statistics (this also prints stats as you wanted)
    

    # Save to JSON file
    with open(output_file, "w", encoding="utf-8") as f:
        json.dump(data, f, indent=4)

    print(f"\n✅ Document statistics exported to '{output_file}'")





doc = DocumentManager("sample.txt")
doc.load_document()
doc.search_documents("chunking")
result = doc.calculate_document_statistics()
print("\nReturned Statistics Dictionary:")
print(result)
print("Document processing completed.")
export_to_json(result, "document_statistics.json")