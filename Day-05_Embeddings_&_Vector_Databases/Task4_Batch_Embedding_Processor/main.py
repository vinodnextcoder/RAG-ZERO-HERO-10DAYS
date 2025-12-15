
from dotenv import load_dotenv
import chromadb
load_dotenv()

class ChromaDBDocument:
    def __init__ (self,collection_name):
        self.collection = collection_name
        print(f"Chromadb initializing")
        self.client = chromadb.Client()

        self.collection = self.client.get_or_create_collection(
            name=collection_name
        )
        print(f"Chromadb initialized with collection: {self.collection}")

        self.content = ""

    def add_context(self):
        # Add documents
        documents = [
            "Python is a high-level programming language",
            "Dogs are loyal and friendly animals",
            "Machine learning is a subset of AI"
        ]

        ids = ["doc1", "doc2", "doc3"]
        metadatas = [
            {"source": "python_book", "page": 1},
            {"source": "animal_guide", "page": 5},
            {"source": "ai_textbook", "page": 10}
        ]

        self.collection.add(
                documents=documents,
                ids=ids,
                metadatas=metadatas
            )

    def search(self):
        # Query for similar documents
        results = self.collection.query(
            query_texts=["programming languages"],
            n_results=2
        )

        print("****************search******************")
        print("Similar documents:")
        for i, doc in enumerate(results['documents'][0]):
            print(f"{i+1}. {doc}")
            print(f"   Metadata: {results['metadatas'][0][i]}")

    def get_by_id(self):
        print("****************search by id******************")
        results = self.collection.get(ids=["doc1","doc2"])
        for doc_id, doc_text, metadata in zip(
            results["ids"], results["documents"], results["metadatas"]
        ):
            print("ID:", doc_id)
            print("Text:", doc_text)
            print("Metadata:", metadata)
            print("-" * 40)

    def get_stats(self):
        """Get collection statistics"""
        print("*******collection state************")
        count = self.collection.count()
        print("total_documents",count)
        return {"total_documents": count}


read_collection = ChromaDBDocument("chromadoclearn")
read_collection.add_context()
read_collection.search()
read_collection.get_by_id()
read_collection.get_stats()
