def is_alive(game_statistics: dict) -> bool:
    return game_statistics["lives"] > 0


def game_status(game_statistics: dict) -> None:

    if is_alive(game_statistics):
        print(f"Verbleibende Leben: {game_statistics['lives']}")  # dani
    else:
        ausgabe = "Du hast alle deine Leben aufgebraucht!"
        print(ausgabe)  # dani


# HAUPTSPIEL-SCHLEIFE (+Konsolen-Test)
def life_loop(game_statistics, ai_input: str) -> dict:
    # ai_input: JA/NEIN/WARM/SEHR_WARM/KALT/Hilfe

    if ai_input == "JA":
        game_statistics["tries"] += 1
        game_statistics["win"] = 1
    if ai_input == "NEIN":
        game_statistics["tries"] += 1
        game_statistics["no"] += 1
        game_statistics["lives"] -= 1
        return game_statistics
    if ai_input == "WARM":
        game_statistics["tries"] += 1
        game_statistics["warm"] += 1
        game_statistics["lives"] -= 1
    if ai_input == "SEHR_WARM":
        game_statistics["tries"] += 1
        game_statistics["hot"] += 1
    if ai_input == "KALT":
        game_statistics["tries"] += 1
        game_statistics["cold"] += 1
        game_statistics["lives"] -= 1
    if ai_input == "Hilfe":
        game_statistics["hints"] += 1
        game_statistics["lives"] -= 1

    return game_statistics
