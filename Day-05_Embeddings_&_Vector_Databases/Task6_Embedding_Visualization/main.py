from dotenv import load_dotenv
import chromadb
import numpy as np
import matplotlib.pyplot as plt
from sklearn.decomposition import PCA
from sklearn.manifold import TSNE

load_dotenv()


class ChromaDBDocument:
    def __init__(self, collection_name):
        print("Chromadb initializing...")
        self.client = chromadb.Client()
        self.collection = self.client.get_or_create_collection(
            name=collection_name
        )
        print(f"Chromadb initialized with collection: {collection_name}")

    def add_context(self):
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
        results = self.collection.query(
            query_texts=["programming languages"],
            n_results=2
        )

        print("\n*************** SEARCH RESULTS ***************")
        for i, doc in enumerate(results["documents"][0]):
            print(f"{i+1}. {doc}")
            print(f"   Metadata: {results['metadatas'][0][i]}")

    def visualize_query_vs_documents(self, query_text, method="pca"):
        # Fetch documents and embeddings
        data = self.collection.get(
            include=["documents", "embeddings"]
        )

        doc_embeddings = np.array(data["embeddings"])
        documents = data["documents"]

        # Get query embedding via ChromaDB
        query_result = self.collection.query(
            query_texts=[query_text],
            n_results=1,
            include=["embeddings"]
        )

        query_embedding = np.array(query_result["embeddings"][0][0])

        # Combine doc + query embeddings
        all_embeddings = np.vstack([doc_embeddings, query_embedding])
        labels = documents + ["QUERY"]

        # Dimensionality reduction
        if method == "pca":
            reducer = PCA(n_components=2)
            reduced = reducer.fit_transform(all_embeddings)
            title = "PCA: Query vs Documents"

        elif method == "tsne":
            n_samples = all_embeddings.shape[0]
            perplexity = min(5, n_samples - 1)

            reducer = TSNE(
                n_components=2,
                perplexity=perplexity,
                random_state=42
            )
            reduced = reducer.fit_transform(all_embeddings)
            title = f"t-SNE: Query vs Documents (perplexity={perplexity})"

        else:
            raise ValueError("method must be 'pca' or 'tsne'")

        # Plot
        plt.figure(figsize=(8, 6))

        # Documents
        plt.scatter(
            reduced[:-1, 0],
            reduced[:-1, 1],
            label="Documents"
        )

        # Query
        plt.scatter(
            reduced[-1, 0],
            reduced[-1, 1],
            marker="X",
            s=200,
            label="Query"
        )

        for i, label in enumerate(labels):
            name = "QUERY" if label == "QUERY" else f"doc{i+1}"
            plt.annotate(name, (reduced[i, 0], reduced[i, 1]))

        plt.title(title)
        plt.xlabel("Dimension 1")
        plt.ylabel("Dimension 2")
        plt.legend()
        plt.grid(True)
        plt.show()


# -------------------- RUN --------------------

read_collection = ChromaDBDocument("chromadoclearn")
read_collection.add_context()
read_collection.search()

read_collection.visualize_query_vs_documents(
    query_text="programming languages",
    method="pca"
)

read_collection.visualize_query_vs_documents(
    query_text="programming languages",
    method="tsne"
)
