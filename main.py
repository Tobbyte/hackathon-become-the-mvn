"""An interactive, llm based Wikipedia game."""

from base_app.base_app import run_game

# Start screen
# Show menu with options (Spielregel und Erklärung)
#
# Call Wikipedia page (Title: something) -> wiki-calls
# Parse result (take only the header) from wiki call to dictionary -> wiki-calls
#


def main() -> None:
    """Orchestrate initialization, run the game."""
    #Rolenaufteilung
    # Wikipedia: Vincent, Jan
    # LLM: Armel, Daniella

    #Rules:
    # In branches arbeiten!

    # ____
    # init if any here
    run_game()


if __name__ == "__main__":
    main()
