import os
import random

from dotenv import load_dotenv
from openai import OpenAI
from personas.py import PERSONAS

from ai.config import STATIC_GPT_PROMPT

load_dotenv()
api_key = os.getenv("OPENAI_API_KEY")

client = OpenAI()

temp_context = """
Der Leopard (Panthera pardus), auch Panther, ist eine Art aus der Familie der Katzen, die in Afrika und Asien verbreitet ist. Darüber hinaus kommt sie auch im Kaukasus vor. Der Leopard ist nach Tiger, Löwe, Jaguar und Puma die fünftgrößte Katzenart. Auf der Roten Liste gefährdeter Arten der IUCN sind Leoparden in der Vorwarnliste als Vulnerable ‚gefährdet‘ klassifiziert.[1]
Leoparden haben von allen sieben Großkatzen das größte Verbreitungsgebiet, sie leben in Afrika und Asien. Sie sind Raubtiere und Einzelgänger.
Die Fellzeichnung ist je nach Unterart oft sehr verschieden, aber auch innerhalb eines Gebietes treten individuelle Unterschiede auf. Fast immer zeigt das Fell Rosetten. In großen Höhenlagen und im tropischen Regenwald findet man manchmal Schwärzlinge, die auch Schwarzer Panther genannt werden. Die Ausprägung des schwarzen Fells ist erblich und wird über ein einziges Gen (monogenetisch) rezessiv vererbt.
"""

# question = STATIC_GPT_PROMPT + generate_persona()


def generate_persona():
    random_persona = random.choice(list(PERSONAS.keys()))
    persona_description = PERSONAS[random_persona]
    return random_persona, persona_description


def get_response(context: str, question: str) -> str:

    response = client.responses.create(
        model="gpt-5-nano",
        input=[
            {"role": "system", "content": question},
            {"role": "user", "content": context},
        ],
    )
    return response


def get_initial_clou(context: str = temp_context) -> str:
    persona = generate_persona()
    initial_clou = get_response(persona + STATIC_GPT_PROMPT, context)
    parsed_response = parse_response(initial_clou)
    return parsed_response


def parse_response(row_response: str) -> str:
    raw_response = row_response.output_text
    return raw_response
