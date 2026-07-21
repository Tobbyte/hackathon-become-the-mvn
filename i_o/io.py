"""All things input-output related."""

from base_app.config import MENU_ITEMS


def output(outp: str) -> None:
    """Print whats give."""
    # TODO: make pretty
    print(outp)


def get_user_input(prompt: str) -> str:
    """Get input from user."""
    # TODO: validate?
    return input(prompt)


def show_menu() -> int:
    """Present the menu to the user."""
    output("Here will be menu\n     1: dummy return '1'\n     2: option2")
    return 1


def clear_lines(num_lines: int) -> None:
    """Delete last num_lines lines from output."""
    for _ in range(num_lines):
        print("\033[F\033[K", end="")


def clear_screen() -> None:
    """Clear terminal, move cursor top left."""
    print("\033[2J\033[H", end="")
    print("\n\n\n\n")  ## spacer


def get_menu_selection() -> int | None:
    """Print the menu to the user, asks for input.

    see base_app.config.MENU_ITEMS
    Options:
        0:  Exit
        1:  tbd
    """
    output("")

    output("Menu:")
    for item in MENU_ITEMS:
        output(item)

    insist_to_quit = False

    while True:
        selection = get_user_input(
            "\nEnter choice (0-11): ",
        ).strip()

        if selection == "" and insist_to_quit:
            return None
        if not selection.isdecimal() or not menu_selection_in_range(selection):
            output(
                "Invalid input (Enter 0 - 11. Try again).\n"
                "Or press ENTER again to quit",
            )
            insist_to_quit = True
        else:
            break

    return int(selection)


def menu_selection_in_range(
    selection: str,
) -> bool:
    """Validate if menu selection is in valid range."""
    max_range = len(MENU_ITEMS) - 1
    min_range = 0
    try:
        int(selection)
    except ValueError:
        return False
    else:
        return min_range <= int(selection) <= max_range
