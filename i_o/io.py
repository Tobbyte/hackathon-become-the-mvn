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
