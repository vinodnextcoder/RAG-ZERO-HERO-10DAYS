import re,os
class DocumentManager:
    def __init__ (self,file_path):
        print("Initializing Document Manager...")
        print(f"File path: {file_path}")
        self.file_path = file_path
        self.files = os.listdir(file_path)
        
    def load_document(self):
        print('------------File Reading-----------------')
        print("Loading document...")
        print(f"Directory path: {self.files}")
        try:
            for file_name in self.files:
                file_name = os.path.join(self.file_path, file_name)    
                with open(file_name, 'r', encoding='utf-8') as file:
                    self.content = file.read()
                    print("Document Content:")
                    print(self.content)
        except FileNotFoundError:
            print(f"The file at {self.files} does not exist.")
        except Exception as e:
            print(f"An error occurred: {e}")


doc = DocumentManager("./data/")
doc.load_document()
