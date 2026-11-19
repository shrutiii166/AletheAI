from langchain_text_splitters import RecursiveCharacterTextSplitter


def split_documents(
    pages: list[dict],
    chunk_size: int = 800,
    chunk_overlap: int = 150,
) -> list[dict]:
    """Split extracted PDF pages into overlapping text chunks."""

    if chunk_size <= 0:
        raise ValueError("Chunk size must be greater than zero.")

    if chunk_overlap < 0 or chunk_overlap >= chunk_size:
        raise ValueError(
            "Chunk overlap must be non-negative and smaller than chunk size."
        )

    splitter = RecursiveCharacterTextSplitter(
        chunk_size=chunk_size,
        chunk_overlap=chunk_overlap,
        add_start_index=True,
    )

    chunks = []

    for page in pages:
        page_chunks = splitter.split_text(page["content"])

        for index, content in enumerate(page_chunks):
            chunks.append(
                {
                    "content": content,
                    "metadata": {
                        **page["metadata"],
                        "chunk_index": index,
                    },
                }
            )

    return chunks