import re,os,json
class DocumentManager:
    def __init__ (self,file_path):
        print("Initializing Document Manager...")
        print(f"File path: {file_path}")
        self.file_path = file_path
        self.files = os.listdir(file_path)
        
    def load_document(self):
        directory_path = self.file_path
        if not os.path.exists(directory_path):
            print(f"Directory not found: {directory_path}")
            return

        if not os.path.isdir(directory_path):
            print(f"Not a directory: {directory_path}")
            return
        self.file_details = []
        for filename in os.listdir(directory_path):
            try:
                full_path = os.path.join(directory_path, filename)
                if not os.path.exists(full_path):
                    print(f"Not found: {full_path}")
                    continue
                
                print(f"Processing: {full_path}")
                with open(full_path, 'r', encoding='utf-8') as file:
                    self.content = file.read()
                    print("Document Content:")
                    print(self.content)
                    self.file_details.append ({
                        "file_name": filename,
                        "statistics": self.content
                    })
                    # calculate_document_statistics(self.content)
            except FileNotFoundError:
                print(f"The file at {self.files} does not exist.")
            except Exception as e:
                print(f"An error occurred: {e}")

    def calculate_document_statistics(self,data):
        content = data
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
        self.result= result
        return result
    
    def export_to_json(self, output_dir):
        """
        Export statistics of each document to separate JSON files
        """

        # ✅ Ensure output directory exists
        os.makedirs(output_dir, exist_ok=True)
        print(f"✅ Output directory ready: '{output_dir}'")

        # ✅ Export each file's statistics separately
        for file_stat in self.file_details:
            file_name = file_stat["file_name"]
            print(f"📄 Exporting statistics for: {file_name}")

            stats = self.calculate_document_statistics(
                file_stat["statistics"]
            )

            json_data = {
                "file_name": file_name,
                "statistics": stats
            }

            # ✅ Create filename
            filename_only, _ = os.path.splitext(file_name)
            output_path = os.path.join(
                output_dir,
                f"{filename_only}_statistics.json"
            )

            # ✅ Write JSON
            with open(output_path, "w", encoding="utf-8") as f:
                json.dump(json_data, f, indent=4)

            print(f"✅ Saved: {output_path}")

        print("\n🎉 All document statistics exported successfully!")
    
    
    def read_file_data(self):
        result = []
        for file_detail in self.file_details:
            print(f"File: {file_detail['file_name']}")
            stats = self.calculate_document_statistics(file_detail['statistics'])
            result.append({
                "file_name": file_detail['file_name'],
                "statistics": stats
            })
            print(f"Statistics: {stats}")
        print("All file statistics calculated.")
        print(result)



            



doc = DocumentManager("./data/")
doc.load_document()
doc.read_file_data()
doc.export_to_json("./output")