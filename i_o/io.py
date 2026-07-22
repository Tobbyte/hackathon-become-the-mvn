"""All things input-output related."""

from base_app.config import MENU_ITEMS
from wiki_calls import category_lists
from wiki_calls.category_lists import categories
from wiki_calls.config import DIFFICULTIES_TOP


def output(outp: str) -> None:
    """Print whats give."""
    # TODO: make pretty
    print(outp)


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
            f"\nEnter choice (0-{len(MENU_ITEMS) - 1}): ",
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

# TODO: die drei hier sind dreckig. menu, category and difficulty
# selectino sollten eine abstraktion sein

def get_category_selection() -> str:
    """Print the available categories, asks for input.

    see wiki_calls.category_list
    """
    output("")
    output("Categories:")
    menu_i = 0
    for cat in categories:
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
                "Or press ENTER again to return to main menu",
            )
            insist_to_quit = True
        else:
            break
    return categories[int(selection) - 1][0]


def get_difficulty_selection() -> str:
    """Print the available categories, asks for input.

    see wiki_calls.category_list
    """
    output("")
    output("Categories:")
    diff_i = 0
    for diff in DIFFICULTIES_TOP:
        diff_i += 1
        output(f"{diff_i}: {diff[0]}")

    insist_to_quit = False

    while True:
        selection = get_user_input(
            f"\nEnter choice (1-{diff_i}): ",
        ).strip()

        if selection == "" and insist_to_quit:
            return None

        if not selection.isdecimal() or not get_difficulty_selection_in_range(
            selection,
            diff_i,
        ):
            output(
                f"Invalid input (Enter 0 - {diff_i}. Try again).\n"
                "Or press ENTER again to return to main menu",
            )
            insist_to_quit = True
        else:
            break

    return DIFFICULTIES_TOP[int(selection) - 1][0]


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
