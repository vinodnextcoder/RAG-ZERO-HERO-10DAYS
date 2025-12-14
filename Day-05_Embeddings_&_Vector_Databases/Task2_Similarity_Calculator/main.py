import numpy as np
from sklearn.metrics.pairwise import cosine_similarity
from sentence_transformers import SentenceTransformer

# Load model once (best practice)
model = SentenceTransformer("all-MiniLM-L6-v2")

def similarity_calculator(text1: str, text2: str):
    """
    Calculate cosine similarity between two texts
    using three different methods.
    """

    # Generate embeddings (1D vectors)
    emb1 = model.encode(text1)
    emb2 = model.encode(text2)

    # ---- Method 1: sentence-transformers utility ----
    st_similarity = model.similarity(
        emb1.reshape(1, -1),
        emb2.reshape(1, -1)
    )[0][0]

    # ---- Method 2: sklearn cosine_similarity ----
    sklearn_similarity = cosine_similarity(
        emb1.reshape(1, -1),
        emb2.reshape(1, -1)
    )[0][0]

    # ---- Method 3: Manual cosine similarity formula ----
    manual_similarity = np.dot(emb1, emb2) / (
        np.linalg.norm(emb1) * np.linalg.norm(emb2)
    )

    print(f"Text 1: {text1}")
    print(f"Text 2: {text2}")
    print(f"SentenceTransformer similarity: {st_similarity:.4f}")
    print(f"Sklearn cosine similarity:      {sklearn_similarity:.4f}")
    print(f"Manual cosine similarity:       {manual_similarity:.4f}")
    print("-" * 50)


# Tests
similarity_calculator("dog", "puppy")
similarity_calculator("dog", "computer")
