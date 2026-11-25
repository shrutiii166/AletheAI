from groq import Groq
from groq import APIConnectionError, APIStatusError, RateLimitError
from functools import lru_cache

from core.config import GROQ_API_KEY, GROQ_MODEL


@lru_cache(maxsize=1)
def get_groq_client():
    """Create and reuse a Groq API client."""

    if not GROQ_API_KEY:
        raise ValueError(
            "GROQ_API_KEY is missing. Please check your environment settings."
        )

    return Groq(
        api_key=GROQ_API_KEY,
        timeout=60.0,
        max_retries=2,
    )


def generate_response(
    prompt: str | None = None,
    messages: list[dict[str, str]] | None = None,
) -> str:
    """Generate an AI response with centralized error handling."""

    if messages is None:
        if not prompt:
            raise ValueError("Please provide a prompt or conversation history.")

        messages = [{"role": "user", "content": prompt}]

    try:
        client = get_groq_client()

        response = client.chat.completions.create(
            model=GROQ_MODEL,
            messages=messages,
            temperature=0.3,
        )

        answer = response.choices[0].message.content

        if not answer or not answer.strip():
            raise RuntimeError(
                "AletheAI couldn't generate a response. Please try again."
            )

        return answer.strip()

    except RateLimitError as exc:
        raise RuntimeError(
            "AletheAI is receiving too many requests right now. "
            "Please wait a moment and try again."
        ) from exc

    except APIConnectionError as exc:
        raise RuntimeError(
            "AletheAI couldn't connect to its AI service. "
            "Please check your internet connection and try again."
        ) from exc

    except APIStatusError as exc:
        raise RuntimeError(
            "AletheAI's AI service encountered an error. "
            "Please try again shortly."
        ) from exc