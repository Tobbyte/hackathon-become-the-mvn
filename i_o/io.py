"""All things input-output related."""

from base_app.config import GAME_RULES, MENU_ITEMS
from i_o.ascii_art import anleitung_ascii
from i_o.colorfull_output import output_colored_text, output_rainbow_text
from wiki_calls import category_lists
from wiki_calls.category_lists import categories
from wiki_calls.config import DIFFICULTIES_TOP


def output(
    outp: str,
    end="\n",
    flush=False,
    *,
    rainbow: bool = False,
) -> None:
    """Print whats give."""
    # TODO: make pretty
    if rainbow:
        output_rainbow_text(outp)
    else:
        output_colored_text(outp, end=end, flush=flush)


def get_user_input(prompt: str) -> str:
    """Get input from user."""
    # TODO: validate?
    return input(prompt)


def clear_lines(num_lines: int) -> None:
    """Delete last num_lines lines from output."""
    for _ in range(num_lines):
        print("\033[F\033[K", end="")


def clear_screen() -> None:
    """Clear terminal, move cursor top left."""
    print("\033[2J\033[H", end="")
    print("\n\n\n\n")  ## spacer


def get_menu_selection_multi(
    menu: tuple[str, list[list]],
    insits_msg: str = "Or press ENTER again to return to main menu",
) -> list | None:
    """Print the available categories, asks for input.

    see wiki_calls.category_list
    """
    menu_name, menu_items = menu
    output("")
    output(f"{menu_name}:")
    menu_i = 0
    for cat in menu_items:
        menu_i += 1
        output(f"{menu_i}: {cat[0]}")

    insist_to_quit = False

    while True:
        selection = get_user_input(
            f"\nEnter choice (1-{menu_i}): ",
        ).strip()

        if selection == "" and insist_to_quit:
            return None

        if not selection.isdecimal() or not get_category_selection_in_range(
            selection,
            menu_i,
        ):
            output(
                f"Invalid input (Enter 0 - {menu_i}. Try again).\n"
                f"{insits_msg}",
                rainbow=True,
            )
            insist_to_quit = True
        else:
            break

    return menu_items[int(selection) - 1]


def get_menu_selection() -> int | None:
    sel = get_menu_selection_multi(("Hauptmenü", MENU_ITEMS))
    if sel is not None:
        return int(sel[1])
    return None


def get_category_selection() -> str | None:
    sel = get_menu_selection_multi(("Kategorien", categories))
    if sel is not None:
        return sel[0]
    return None


def get_difficulty_selection() -> str | None:
    sel = get_menu_selection_multi(("Schwierigkeit", DIFFICULTIES_TOP))
    if sel is not None:
        return sel[0]
    return None


def get_difficulty_selection_in_range(
    selection: str,
    max_range: int,
) -> bool:
    """Validate if menu selection is in valid range."""
    min_range = 1

    try:
        int(selection)
    except ValueError:
        return False
    else:
        return min_range <= int(selection) <= max_range


def get_category_selection_in_range(
    selection: str,
    max_range: int,
) -> bool:
    """Validate if menu selection is in valid range."""
    min_range = 1

    try:
        int(selection)
    except ValueError:
        return False
    else:
        return min_range <= int(selection) <= max_range


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


def output_howto() -> None:
    output(anleitung_ascii)
    output(GAME_RULES, rainbow=True)


def get_ab_choice(prompt: str, opt_a: list[str], opt_b: list[str]) -> bool:
    """Ask user to choose between opt_a and opt_b.

    Returns True for opt_a,
    returns False for opt_b.
    """
    while True:
        user_choice = input(prompt).strip()
        if user_choice not in opt_a and user_choice not in opt_b:
            print(f'Choose "{", ".join(opt_a)}" or "{", ".join(opt_b)}": ')
        else:
            break

    return user_choice in opt_a
