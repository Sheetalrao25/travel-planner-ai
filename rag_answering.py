from sentence_transformers import SentenceTransformer
import faiss
import numpy as np

model = SentenceTransformer("all-MiniLM-L6-v2")

# Load documents
def load_docs(filepath="destination_docs.txt"):
    docs = []
    with open(filepath, "r", encoding="utf-8") as f:
        for line in f:
            if line.strip():
                docs.append(line.strip())
    return docs

# Embed and index
def build_rag_index(docs):
    embeddings = model.encode(docs)
    index = faiss.IndexFlatL2(embeddings[0].shape[0])
    index.add(np.array(embeddings))
    return index, embeddings

# Retrieve top doc + generate answer using local LLM
from transformers import pipeline
llm = pipeline("text2text-generation", model="google/flan-t5-base")

def answer_question(question, docs, index, top_k=3):
    q_embed = model.encode([question])
    distances, indices = index.search(np.array(q_embed), top_k)

    # Search for best match manually by checking which doc contains destination keyword
    question_lower = question.lower()

    for idx in indices[0]:
        candidate = docs[idx]
        if any(word in candidate.lower() for word in question_lower.split()):
            context = candidate
            break
    else:
        context = docs[indices[0][0]]  # fallback

    prompt = (
        f"You are a travel assistant.\n"
        f"Context: {context}\n"
        f"Question: {question}\n"
        f"Answer in 1-2 full informative sentences."
    )
    response = llm(prompt, max_new_tokens=100)[0]["generated_text"]
    return response.strip()

