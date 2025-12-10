import re,os
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
            except FileNotFoundError:
                print(f"The file at {self.files} does not exist.")
            except Exception as e:
                print(f"An error occurred: {e}")

            



doc = DocumentManager("./data/")
doc.load_document()
