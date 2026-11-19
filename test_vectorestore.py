from rag.vector_store import (
    create_vector_store,
    add_chunks,
    search_chunks,
)

# Create a temporary vector store
client, collection = create_vector_store()

# Sample document chunks
chunks = [
    {
        "content": "Regular exercise improves cardiovascular health and strengthens the heart.",
        "metadata": {"source": "fitness_guide.pdf", "page": 1},
    },
    {
        "content": "A balanced diet includes proteins, carbohydrates, healthy fats, vitamins, and minerals.",
        "metadata": {"source": "fitness_guide.pdf", "page": 2},
    },
    {
        "content": "Python is a popular programming language used for data analysis and machine learning.",
        "metadata": {"source": "programming_guide.pdf", "page": 1},
    },
]

# Generate embeddings and store the chunks
stored_count = add_chunks(collection, chunks)
print(f"Chunks stored: {stored_count}")

# Search for relevant information
question = "How can I keep my heart healthy?"

results = search_chunks(collection, question)

print("\nSearch results:")

for result in results:
    print(f"\nSource: {result['metadata']['source']}")
    print(f"Page: {result['metadata']['page']}")
    print(f"Text: {result['content']}")
    print(f"Distance: {result['distance']:.4f}")

# Release the temporary client
del collection
del client