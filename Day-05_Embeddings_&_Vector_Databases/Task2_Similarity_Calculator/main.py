import os
from sklearn.metrics.pairwise import cosine_similarity
import numpy as np
from sentence_transformers import SentenceTransformer

def similarity_calculator():
    model = SentenceTransformer("all-MiniLM-L6-v2")
    text1 = "dog"
    text2 = "puppy"

    query_embedding = model.encode(text1)  # 2D
    doc_embeddings = model.encode(text2)  # 2D
    # using sentence_transformers
    similarities = model.similarity(query_embedding, doc_embeddings)
    print(similarities)

    # using sklearn
    score = cosine_similarity([query_embedding], [doc_embeddings])[0][0]
    print("Cosine similarity:", score)
    #using formula
    cos_sim = np.dot(query_embedding, doc_embeddings) / (np.linalg.norm(query_embedding) * np.linalg.norm(doc_embeddings))

    print("Cosine similarity:", cos_sim)




similarity_calculator()