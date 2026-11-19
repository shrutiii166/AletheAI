from core.llm_connector import generate_response

answer = generate_response(
    "Introduce yourself in one short sentence as the AI assistant "
    "for an application called AletheAI."
)

print("\nAletheAI response:")
print(answer)