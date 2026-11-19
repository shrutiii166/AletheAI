from core.llm_connector import generate_response


POETRY_FEATURES = [
    "Line-by-Line Analysis",
    "Emotional Interpretation",
    "Alternative Interpretations",
    "Poem to Me",
    "Interpretation & Discussion",
    "Talk to the Poet",
]


def analyze_poetry(feature: str, question: str, context: str) -> str:
    prompt = f"""
You are AletheAI's Poetry Companion.

Help the reader explore poetry and lyrics with sensitivity,
literary understanding, and thoughtful interpretation.

Selected feature: {feature}

Reader's request:
{question}

Retrieved passages from the uploaded work:
{context}

Instructions:
- Ground interpretations in the supplied text.
- Explain imagery, symbolism, tone, language, and subtext where relevant.
- Allow multiple interpretations when the text is ambiguous.
- Do not claim to know the poet's actual emotions or intentions.
- Cite page numbers when available.
- Never invent quotations or lines.
"""
    return generate_response(prompt=prompt)