import re
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
    def convert_to_lowercase(self):
        print("Converting text to lowercase...")
        text = self.content
        return text.lower()
    def remove_punctuation(self,text):
        print("Removing punctuation from text...")
        return re.sub(r'[^\w\s]', '', text)
    def remove_extra_whitespace(self,text):
        print("Removing extra whitespace from text...")
        return ' '.join(text.split())
    def remove_leading_trailing_whitespace(self,text):
        print("Removing leading and trailing whitespace from text...")
        return text.strip()
    def remove_stopwords(self,text,stopwords):
        print("Removing stopwords from text...")
        words = text.split()
        filtered_words = [word for word in words if word.lower() not in stopwords]
        return ' '.join(filtered_words)
    
doc = DocumentManager("sample.txt")
doc.load_document()
convert_to_lowercase = doc.convert_to_lowercase()
print("----------------------------")
print("Lowercase Text:")
print(convert_to_lowercase)
print("----------------------------")
print("Punctuation Removed Text:")
punctuation_removed = doc.remove_punctuation(convert_to_lowercase)
print(punctuation_removed)
print("----------------------------")
print("Extra Whitespace Removed Text:")
whitespace_removed = doc.remove_extra_whitespace(punctuation_removed)
print(whitespace_removed)
print("----------------------------")
print("Leading and Trailing Whitespace Removed Text:")
final_text = doc.remove_leading_trailing_whitespace(whitespace_removed)
print(final_text)
print("----------------------------")
stopwords = {"the", "is", "in", "and", "to", "a"}
stopwords_removed = doc.remove_stopwords(final_text, stopwords)
print("Stopwords Removed Text:")
print(stopwords_removed)