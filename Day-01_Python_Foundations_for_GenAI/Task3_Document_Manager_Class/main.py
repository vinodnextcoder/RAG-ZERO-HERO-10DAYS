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




doc = DocumentManager("sample.txt")
doc.load_document()