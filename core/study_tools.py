from core.llm_connector import generate_response
from rag.vector_store import search_chunks
from core.config import TOP_K_RESULTS


def generate_study_response(
    collection,
    query: str,
    instructions: str,
) -> str:
    """Generate a study response using relevant chunks from uploaded material."""

    retrieved_chunks = search_chunks(
        collection,
        query,
        top_k=TOP_K_RESULTS,
    )

    if not retrieved_chunks:
        return "I couldn't find relevant information in your uploaded study material."

    context_parts = []

    for chunk in retrieved_chunks:
        metadata = chunk["metadata"]
        source = metadata.get("source", "Unknown")
        page = metadata.get("page", "Unknown")

        context_parts.append(
            f"Source: {source}\n"
            f"Page: {page}\n"
            f"Content:\n{chunk['content']}"
        )

    context = "\n\n---\n\n".join(context_parts)

    messages = [
        {
            "role": "system",
            "content": (
                "You are AletheAI's Study Assistant. "
                f"{instructions} "
                "Use only the provided study material. "
                "Do not invent information. "
                "If the context is insufficient, say so."
            ),
        },
        {
            "role": "user",
            "content": f"Study material:\n\n{context}\n\nTask:\n{query}",
        },
    ]

    return generate_response(messages=messages)


def generate_revision_notes(collection) -> str:
    """Generate exam-focused revision notes from uploaded study material."""

    return generate_study_response(
        collection=collection,
        query=(
            "Create concise revision notes covering the most important topics, "
            "definitions, key facts, and concepts from the uploaded study material."
        ),
        instructions=(
            "Create well-organized revision notes using headings, bullet points, "
            "and numbered lists where appropriate. Highlight important definitions, "
            "key facts, and relationships between concepts. Keep the notes useful "
            "for exam preparation without unnecessary repetition."
        ),
    )


def generate_flashcards(collection) -> str:
    """Generate study flashcards from uploaded study material."""

    return generate_study_response(
        collection=collection,
        query=(
            "Create 10 flashcards from the uploaded study material. "
            "Each flashcard must have a question and its corresponding answer."
        ),
        instructions=(
            "Create useful flashcards for active recall and exam preparation. "
            "Focus on important concepts, definitions, facts, and relationships. "
            "Format each flashcard as 'Question:' followed by 'Answer:'. "
            "Number the flashcards clearly. Keep answers accurate and concise. "
            "Do not introduce information that is absent from the provided context."
        ),
    )

def answer_study_question(collection, question: str) -> str:
    """Answer a question using uploaded study material."""

    return generate_study_response(
        collection=collection,
        query=question,
        instructions=(
            "Answer the student's question clearly and accurately using the "
            "provided study material. Explain important points and include "
            "relevant examples only when supported by the context. If the "
            "material does not contain enough information, say so."
        ),
    )


def explain_concept_simply(collection, concept: str) -> str:
    """Explain a concept in beginner-friendly language."""

    return generate_study_response(
        collection=collection,
        query=f"Explain this concept simply: {concept}",
        instructions=(
            "Explain concepts in simple, beginner-friendly language. Use short "
            "sentences, break down difficult terminology, and include a simple "
            "analogy or example when appropriate and supported by the context. "
            "Preserve the scientific or technical meaning."
        ),
    )


def generate_practice_quiz(collection, topic: str = "") -> str:
    """Generate a practice quiz from uploaded study material."""

    query = (
        f"Create a practice quiz about {topic}."
        if topic.strip()
        else "Create a practice quiz covering the important topics in the study material."
    )

    return generate_study_response(
        collection=collection,
        query=query,
        instructions=(
            "Create 10 practice questions based on the provided material. "
            "Include a mix of multiple-choice and short-answer questions where "
            "possible. For multiple-choice questions, provide four options. "
            "Place the answer key after all questions, with brief explanations. "
            "Do not include answers immediately after individual questions. "
            "Do not invent facts outside the provided context."
        ),
    )


def break_down_topics(collection, topic: str = "") -> str:
    """Break study material into smaller, manageable topics."""

    query = (
        f"Break down this topic into smaller learning sections: {topic}"
        if topic.strip()
        else "Identify and break down the main topics in the study material."
    )

    return generate_study_response(
        collection=collection,
        query=query,
        instructions=(
            "Organize the material into a logical learning outline. Divide broad "
            "topics into smaller subtopics, list the key concepts under each, "
            "and explain briefly what each section covers. Present the topics "
            "in a sensible learning order."
        ),
    )


def explain_differently(collection, concept: str, explanation: str = "") -> str:
    """Explain a concept using a different approach."""

    query = (
        f"Explain this concept differently: {concept}\n"
        f"Previous explanation to improve upon: {explanation}"
        if explanation.strip()
        else f"Explain this concept using a different approach: {concept}"
    )

    return generate_study_response(
        collection=collection,
        query=query,
        instructions=(
            "Provide a genuinely different explanation of the concept. If a "
            "previous explanation is supplied, avoid simply repeating it. Try "
            "a different structure, analogy, example, or step-by-step approach. "
            "Keep the explanation accurate and grounded in the study material."
        ),
    )


def estimate_study_difficulty(collection, topic: str = "") -> str:
    """Estimate how challenging a topic may be to learn."""

    query = (
        f"Estimate the learning difficulty of this topic: {topic}"
        if topic.strip()
        else "Estimate the learning difficulty of the main topics in the study material."
    )

    return generate_study_response(
        collection=collection,
        query=query,
        instructions=(
            "Assess the topic's likely learning difficulty as Easy, Moderate, "
            "or Challenging. Explain the rating using factors such as conceptual "
            "complexity, prerequisite knowledge, terminology, and the number of "
            "ideas that must be connected. Identify potentially difficult parts "
            "and suggest how to approach them. Base the assessment on the provided "
            "material, and clarify that difficulty can vary between learners."
        ),
    )