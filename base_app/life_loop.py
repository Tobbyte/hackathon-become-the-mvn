def is_alive(current_lives: int) -> bool:
    return current_lives > 0


def lose_life(current_lives: int, amount: int = 1) -> int:
    new_lives = max(0, current_lives - amount)

    if not is_alive(new_lives):
        ausgabe ="Du hast alle deine Leben aufgebraucht!"
        print(ausgabe)  # dani
    else:
        ausgabe =f"Verbleibende Leben: {new_lives}"
        print(ausgabe)  # dani

    return new_lives


def request_hint(current_lives: int) -> tuple[int, bool]:
    if current_lives <= 1:
        ausgabe ="Du hast nicht genug Leben für eine Hilfestellung übrig!"
        print(ausgabe)  # dani
        return current_lives, False

    ausgabe ="\n💡 [Hilfe]: Hier ist deine Hilfestellung..."
    print(ausgabe)  # dani
    new_lives = lose_life(current_lives, amount=1)
    return new_lives, True


# HAUPTSPIEL-SCHLEIFE (+Konsolen-Test)
def life_loop():
    while True:
        lives = 10
        rounds = 1
        help = 0
        ausgabe ="\n=+= Du startest eine neue Runde! =+="

        while is_alive(lives):
            ausgabe =f"\n[Leben übrig: {lives}]"
            print(ausgabe)  # dani
            check_answer =  #check answer ist = Funktion
            help = #check help ist = Funktion
            rounds += 1
            if check_answer:
                ausgabe = "Gut gemacht, deine Antwort war richtig!"
                print(ausgabe)  # dani
                break

            if check_answer is False:
                lives = lose_life(lives)

            if help:
                lives, hint_given = request_hint(lives)
                help += 1


        if is_alive(lives):
            ausgabe ="\nHerzlichen Glückwunsch, du hast diese Runde gewonnen!"
            print(ausgabe)  # dani

        replay = (
            input("\nWillst du noch eine Runde spielen? (ja/nein): ").strip().lower()
        )
        if replay not in ["ja", "nein"]:
            ausgabe ="Danke fürs Spielen von „Became a Nerd“. Bis bald!"
            print(ausgabe)  # dani
life_loop()