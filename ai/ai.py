import os

from config import (
    GAME_PERSONA,
    GAME_SYSTEM_KONTEXT,
    NOTE_QUESTION,
    WIKI_CONTEXT,
    WIKI_PERSONA,
    WIKI_QUESTION,
)
from dotenv import load_dotenv
from openai import OpenAI

load_dotenv()
api_key = os.getenv("OPENAI_API_KEY")

client = OpenAI()


def generate_persona(persona: str = WIKI_PERSONA):
    common_role = "Du bist der Spielleiter des Ratespiels.\n"
    return common_role + persona


def ask_llm(
    persona: str,
    context: str = WIKI_CONTEXT,
    question: str = WIKI_QUESTION,
    previous_response_id: str | None = None,
):
    """Streamt antwort. Gibt (voller_text, response_id) zurück."""
    # previous_response_id verkettet den Call an eine frühere Response, damit die
    # KI sich an den bisherigen Gesprächsverlauf erinnert (Server-seitig verwaltet).

    full_text = ""
    response_id = None

    system_prompt = f"""
    {persona}.
    
    Verwende zur Beantwortung der Frage des Nutzers AUSSCHLIESSLICH den folgenden Kontext.
    
    Kontext:
    {context}    
    """

    with client.responses.stream(
        model="gpt-5-nano",
        input=[
            {
                "role": "system",
                "content": [
                    {
                        "type": "input_text",
                        "text": system_prompt,
                    }
                ],
            },
            {
                "role": "user",
                "content": [
                    {
                        "type": "input_text",
                        "text": question,
                    }
                ],
            },
        ],
        reasoning={"effort": "low"},
        previous_response_id=previous_response_id,
    ) as stream:
        for event in stream:
            if event.type == "response.output_text.delta":
                # print(event.delta, end="", flush=True)
                full_text += event.delta
            elif event.type == "response.completed":
                response_id = event.response.id
                print()

        return full_text, response_id


def get_initial_clou(context: str = WIKI_CONTEXT) -> str:
    persona = generate_persona()
    initial_clou = ask_llm(persona, context)
    parsed_response = parse_response(initial_clou)
    return parsed_response


def parse_response(row_response) -> str:
    raw_response = row_response.output_text
    return raw_response


wiki_summary, last_id = ask_llm(generate_persona())
print(wiki_summary)

context = GAME_SYSTEM_KONTEXT.format(summary=wiki_summary, solution="Leopard")
user_question = "Bin ich ein Leopard?"  # -> Ja
# user_question = "Bin ich ein Tier?"  # -> WARM
# user_question = "Bin ich eine Katze?"  # -> WARM
# user_question = "Bin ich ein Mensch?"  # -> NEIN
game_response, last_id = ask_llm(GAME_PERSONA, context, user_question, last_id)
print("Game response: ", game_response)

note_response, last_id = ask_llm(WIKI_PERSONA, WIKI_CONTEXT, NOTE_QUESTION, last_id)
print(f"Note response: \n{note_response}")
