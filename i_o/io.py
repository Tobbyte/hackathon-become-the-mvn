"""All things input-output related."""


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
