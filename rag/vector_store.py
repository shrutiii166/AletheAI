import chromadb

from rag.embeddings import embed_texts

def create_vector_store():
    """Create a uniquely named in-memory ChromaDB collection."""
    import uuid

    client = chromadb.EphemeralClient()

    collection_name = f"aletheai_{uuid.uuid4().hex}"

    collection = client.create_collection(
        name=collection_name,
        metadata={"hnsw:space": "cosine"},
    )

    return client, collection

def add_chunks(collection, chunks: list[dict]) -> int:
    """Embed and store document chunks with unique IDs."""
    import uuid

    if not chunks:
        return 0

    texts = [chunk["content"] for chunk in chunks]
    embeddings = embed_texts(texts)

    document_id = uuid.uuid4().hex

    collection.add(
        ids=[
            f"{document_id}_chunk_{i}"
            for i in range(len(chunks))
        ],
        documents=texts,
        embeddings=embeddings,
        metadatas=[chunk["metadata"] for chunk in chunks],
    )

    return len(chunks)

def search_chunks(
    collection,
    query: str,
    top_k: int = 4,
) -> list[dict]:
    """Find the most relevant chunks for a question."""
    if not query.strip() or collection.count() == 0:
        return []

    query_embedding = embed_texts([query])[0]

    results = collection.query(
        query_embeddings=[query_embedding],
        n_results=min(top_k, collection.count()),
    )

    matches = []

    if not results["documents"] or not results["documents"][0]:
        return matches

    for i, document in enumerate(results["documents"][0]):
        matches.append({
            "content": document,
            "metadata": results["metadatas"][0][i],
            "distance": results["distances"][0][i],
        })

    return matches