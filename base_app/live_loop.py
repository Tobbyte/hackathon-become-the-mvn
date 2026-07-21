def is_alive(current_lives: int) -> bool:
    return current_lives > 0


def lose_life(current_lives: int, amount: int = 1) -> int:
    new_lives = max(0, current_lives - amount)

    if not is_alive(new_lives):
        print("Du hast alle deine Leben aufgebraucht!")
    else:
        print(f"Verbleibende Leben: {new_lives}")

    return new_lives


def request_hint(current_lives: int) -> tuple[int, bool]:
    if current_lives <= 1:
        print("Du hast nicht genug Leben für eine Hilfestellung übrig!")
        return current_lives, False

    print("\n💡 [Hilfe]: Hier ist deine Hilfestellung...")
    new_lives = lose_life(current_lives, amount=1)
    return new_lives, True


# HAUPTSPIEL-SCHLEIFE (+Konsolen-Test)

if __name__ == "__main__":
    while True:
        lives = 10
        tries_left = 10

        print("\n=+= Du startest eine neue Runde! =+=")

        while tries_left > 0 and is_alive(lives):
            print(f"\n[Versuche übrig: {tries_left} | Leben: {lives}]")
            test_answer = input("Antwort (Ja / Nein / Hilfe): ").strip().lower()

            if test_answer in [
                "ja",
                "Ja",
                "Richtig",
                "richtig",
            ]:  # True und False nehmen ?
                print("Gut gemacht, deine Antwort war richtig!")

            elif test_answer in ["nein", "Ja", "falsch", "Falsch"]:
                lives = lose_life(lives)
                tries_left -= 1

            elif test_answer in ["Hilfe", "hilfe"]:
                lives, hint_given = request_hint(lives)

            else:
                print("Ungültige Eingabe! Wählen Sie: ja, nein oder Hilfe.")

        if is_alive(lives):
            print("\nHerzlichen Glückwunsch, du hast diese Runde gewonnen!")

        replay = (
            input("\nWIllst du noch eine Runde spielen? (ja/nein): ").strip().lower()
        )
        if replay not in ["ja", "nein"]:
            print("Danke fürs Spielen von „Became a Nerd“. Bis bald!")
