from groq import Groq

from core.config import GROQ_API_KEY, GROQ_MODEL


def get_groq_client():
    """Create and return a Groq API client."""

    if not GROQ_API_KEY:
        raise ValueError(
            "GROQ_API_KEY is missing. Check your project's .env file."
        )

    return Groq(api_key=GROQ_API_KEY)


def generate_response(
    prompt: str | None = None,
    messages: list[dict[str, str]] | None = None,
) -> str:
    """Generate an AI response from a prompt or conversation history."""

    if messages is None:
        if not prompt:
            raise ValueError("Provide either a prompt or a message history.")

        messages = [
            {"role": "user", "content": prompt}
        ]

    client = get_groq_client()

    response = client.chat.completions.create(
        model=GROQ_MODEL,
        messages=messages,
        temperature=0.3,
    )

    return response.choices[0].message.content or ""