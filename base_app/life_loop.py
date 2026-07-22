from datetime import datetime

from ai.ai import ask_llm, generate_persona
from ai.config import GAME_PERSONA, GAME_SYSTEM_KONTEXT, HINT_QUESTION
from i_o.ascii_art import conspiracy_theorist_ascii, pirat_ascii, yoda_ascii
from i_o.io import get_user_input, output
from multiplayer.multiplayer import create_timestamp

PERSONA_TO_ASCII = {
    "conspiracy_theorist": conspiracy_theorist_ascii,
    "pirat_persona": pirat_ascii,
    "yoda_persona": yoda_ascii,
}

def interact_with_user(wiki_article: dict) -> dict:
    game_statistics = {
        "tries": 0,
        "help_needed": 0,
        "no": 0,
        "warm": 0,
        "hot": 0,
        "cold": 0,
        "win": 0,
        "lives": 10,
        "wrong_answers": 0,
        "timestamp_start": create_timestamp(),
        "timestamp_end": None,
        "title": wiki_article["title"],
    }
    title = wiki_article["title"]
    full_article = wiki_article["full_article"]
    persona, persona_name = generate_persona()
    wiki_summary, last_id = ask_llm(persona, full_article)
    output(PERSONA_TO_ASCII[persona_name] + "\n" + wiki_summary)

    while True:
        game_status(game_statistics)
        user_input = ""
        while True:
            user_input = get_user_input("Rate mal... (exit | hilfe) ")
            if not user_input:
                output("Bitte gebe eine Antwort ein!")
            else:
                break
        # Wenn der user nur 1 Versuch hat, darf er keine Hilfe mehr holen
        if user_input.lower() == "hilfe":
            if game_statistics["lives"] == 1:
                output("Du hast nicht genug Leben für eine Hilfestellung übrig!")
                # continue
            else:
                hint_response, last_id = ask_llm(
                    persona, wiki_summary, HINT_QUESTION, last_id
                )
                output(f"Hint response: \n{hint_response}\n")
                game_statistics = life_loop(game_statistics, "Hilfe")

        elif user_input.lower() == "exit":
            game_statistics["timestamp_end"] = create_timestamp()
            break
        else:
            context = GAME_SYSTEM_KONTEXT.format(summary=wiki_summary, solution=title)
            game_response, last_id = ask_llm(GAME_PERSONA, context, user_input, last_id)
            output(f"Game response: {game_response}")
            print()
            print()
            game_statistics = life_loop(game_statistics, game_response)
            if game_response == "JA":
                output("Congratulations! You win!")
                game_statistics["timestamp_end"] = create_timestamp()
                break
            if not is_alive(game_statistics):
                game_status(game_statistics)
                game_statistics["timestamp_end"] = create_timestamp()
                break

    return game_statistics


def is_alive(game_statistics: dict) -> bool:
    return game_statistics["lives"] > 0


def game_status(game_statistics: dict) -> None:

    if is_alive(game_statistics):
        output(f"Verbleibende Leben: {game_statistics['lives']}")  # dani
    else:
        ausgabe = "Du hast alle deine Leben aufgebraucht!"
        output(ausgabe)  # dani


# HAUPTSPIEL-SCHLEIFE (+Konsolen-Test)
def life_loop(game_statistics, ai_input: str) -> dict:
    # ai_input: JA/NEIN/WARM/SEHR_WARM/KALT/Hilfe

    if ai_input == "JA":
        game_statistics["tries"] += 1
        game_statistics["win"] = 1
    if ai_input == "NEIN":
        game_statistics["wrong_answers"] += 1
        game_statistics["tries"] += 1
        game_statistics["no"] += 1
        game_statistics["lives"] -= 1
        return game_statistics
    if ai_input == "WARM":
        game_statistics["wrong_answers"] += 1
        game_statistics["tries"] += 1
        game_statistics["warm"] += 1
        game_statistics["lives"] -= 1
    if ai_input == "SEHR_WARM":
        game_statistics["wrong_answers"] += 1
        game_statistics["tries"] += 1
        game_statistics["hot"] += 1
    if ai_input == "KALT":
        game_statistics["wrong_answers"] += 1
        game_statistics["tries"] += 1
        game_statistics["cold"] += 1
        game_statistics["lives"] -= 1
    if ai_input == "Hilfe":
        game_statistics["help_needed"] += 1
        game_statistics["lives"] -= 1

    return game_statistics
