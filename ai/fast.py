import os

from config import STATIC_GPT_PROMPT
from dotenv import load_dotenv
from openai import OpenAI

load_dotenv()
api_key = os.getenv("OPENAI_API_KEY")

client = OpenAI()

temp_context = """
Der Leopard (Panthera pardus), auch Panther, ist eine Art aus der Familie der Katzen, die in Afrika und Asien verbreitet ist. Darüber hinaus kommt sie auch im Kaukasus vor. Der Leopard ist nach Tiger, Löwe, Jaguar und Puma die fünftgrößte Katzenart. Auf der Roten Liste gefährdeter Arten der IUCN sind Leoparden in der Vorwarnliste als Vulnerable ‚gefährdet‘ klassifiziert.[1]
Leoparden haben von allen sieben Großkatzen das größte Verbreitungsgebiet, sie leben in Afrika und Asien. Sie sind Raubtiere und Einzelgänger.
Die Fellzeichnung ist je nach Unterart oft sehr verschieden, aber auch innerhalb eines Gebietes treten individuelle Unterschiede auf. Fast immer zeigt das Fell Rosetten. In großen Höhenlagen und im tropischen Regenwald findet man manchmal Schwärzlinge, die auch Schwarzer Panther genannt werden. Die Ausprägung des schwarzen Fells ist erblich und wird über ein einziges Gen (monogenetisch) rezessiv vererbt.
"""


def generate_persona():
    return """Du bist ein betrunkener Pirat in einer Taverne und veranstaltest ein Ratespiel."""


def get_response(
    system_prompt: str,
    user_content: str,
    previous_response_id: str | None = None,
):
    """Streamt antwort. Gibt (voller_text, response_id) zurück."""
    # previous_response_id verkettet den Call an eine frühere Response, damit die
    # KI sich an den bisherigen Gesprächsverlauf erinnert (Server-seitig verwaltet).

    full_text = ""
    response_id = None

    with client.responses.stream(
        model="gpt-5-nano",
        input=[
            {"role": "system", "content": system_prompt},
            {"role": "user", "content": user_content},
        ],
        reasoning={"effort": "minimal"},
        previous_response_id=previous_response_id,
    ) as stream:
        for event in stream:
            if event.type == "response.output_text.delta":
                print(event.delta, end="", flush=True)
                full_text += event.delta
            elif event.type == "response.completed":
                response_id = event.response.id
                print()

    return full_text, response_id


def get_initial_clou(context: str = temp_context):
    persona = generate_persona()
    system_prompt = persona + STATIC_GPT_PROMPT
    return get_response(system_prompt, context)


def get_followup_answer(
    context: str,
    question: str,
    previous_response_id: str | None,
):
    """Beantwortet Folgefragen des Nutzers (z.B. 'Bin ich lebendig?')."""
    persona = generate_persona()
    system_prompt = persona + STATIC_GPT_PROMPT
    user_content = (
        f"Lösungswort/Kontext:\n{context}\n\nSpielerfrage: {question}"
    )
    return get_response(
        system_prompt,
        user_content,
        previous_response_id=previous_response_id,
    )


clou, last_id = get_initial_clou(temp_context)
while True:
    dev_input = input("\nfrage ")
    answer, last_id = get_followup_answer(
        temp_context,
        dev_input,
        previous_response_id=last_id,
    )
