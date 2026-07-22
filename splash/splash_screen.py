"""Show a welcome splash_screen."""

from base_app.config import WELCOME_MSG_2
from i_o.io import clear_lines, output
from splash.ascii import PROCEED, SPLASH_MSG


def show_splashscreen() -> None:
    """Draw an ascii art welcome splash."""
    output(SPLASH_MSG, rainbow=True)
    lines = SPLASH_MSG.count("\n")

    welcome = WELCOME_MSG_2 + "\n"
    lines += welcome.count("\n")
    output(welcome, rainbow=True)

    proceed = PROCEED + "\n"
    lines += proceed.count("\n")
    _ = input(
        proceed,
    )
    lines += 1
    clear_lines(lines)
