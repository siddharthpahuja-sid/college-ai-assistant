import faiss
import numpy as np
def create_index(embeddings):
    embeddings=np.array(embeddings).astype("float32")
    dimension=embeddings.shape[1]
    dimension=len(embeddings[0])
    index=faiss.IndexFlatL2(dimension)
    index.add(embeddings)
    return(index)


def search_similar(query_vector, index, chunks):
    query_vector = np.array([query_vector]).astype("float32")
    distances, indices = index.search(query_vector, 2)
    results = []
    for i in indices[0]:
        results.append(chunks[i])
    return results