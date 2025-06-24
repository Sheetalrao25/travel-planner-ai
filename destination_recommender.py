from sentence_transformers import SentenceTransformer
import faiss
import numpy as np

# Load a lightweight embedding model
model = SentenceTransformer("all-MiniLM-L6-v2")

# Read destination descriptions
def load_destinations(filepath="destination_data.txt"):
    destinations = []
    with open(filepath, "r", encoding="utf-8") as f:
        for line in f:
            if ':' in line:
                name, desc = line.strip().split(":", 1)
                destinations.append((name.strip(), desc.strip()))
    return destinations

# Create FAISS index
def create_faiss_index(destinations):
    texts = [desc for _, desc in destinations]
    embeddings = model.encode(texts)
    index = faiss.IndexFlatL2(embeddings[0].shape[0])
    index.add(np.array(embeddings))
    return index, embeddings, texts

# Recommend destinations by comparing interest sentence with index
def recommend_destinations(user_interests, destinations, index, texts, top_k=2):
    query = " ".join(user_interests)
    query_embedding = model.encode([query])
    distances, indices = index.search(np.array(query_embedding), top_k)
    recommended = [destinations[i][0] for i in indices[0]]
    return recommended
