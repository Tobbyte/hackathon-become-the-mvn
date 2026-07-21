"""Show a welcome splash_screen."""

from i_o.io import clear_lines, output
from splash.ascii import SPLASH_MSG, WELCOME_MSG


def show_splashscreen() -> None:
    """Draw an ascii art welcome splash."""
    output(SPLASH_MSG)
    lines = SPLASH_MSG.count("\n")
    welcome_msg = WELCOME_MSG + "\n"
    lines += welcome_msg.count("\n")
    _ = input(
        welcome_msg,
    )
    lines += 1
    clear_lines(lines)
