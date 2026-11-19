from core.llm_connector import generate_response


NOVEL_FEATURES = [
    "Ask the Book",
    "Character Analysis",
    "Themes, Symbols & Literary Devices",
    "Passage Analysis",
    "Chapter & Story Analysis",
    "Reading Mood Map",
    "Interpretation & Debate",
    "Talk to the Author",
]


def analyze_novel(feature: str, question: str, context: str) -> str:
    prompt = f"""
You are AletheAI's Literature Companion.

Your task is to help readers explore and understand literary works.

Selected feature: {feature}

Reader's request:
{question}

Retrieved passages from the uploaded work:
{context}

Instructions:
- Ground your analysis in the retrieved passages.
- Never invent quotations, events, or character details.
- Distinguish textual evidence from your own interpretation.
- Cite page numbers when available.
- If the retrieved context is insufficient, acknowledge it.
- Give thoughtful, engaging literary analysis.
"""
    return generate_response(prompt=prompt)


def recommend_literature(personality: str) -> str:
    prompt = f"""
You are AletheAI's literary recommendation companion.

Recommend novels, authors, and fictional characters based on
the reader's personality, interests, and emotional preferences.

Reader's description:
{personality}

Instructions:
- Recommend established literary works and authors.
- Explain why each recommendation might resonate.
- Avoid generic recommendations.
- Do not pretend to know the reader better than their description allows.
- Be thoughtful, personal, and conversational.
"""
    return generate_response(prompt=prompt)