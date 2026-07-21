"""Show a welcome splash_screen."""

from splash.ascii import SPLASH_MSG, WELCOME_MSG


def show_splashscreen() -> None:
    """Draw an ascii art welcome splash."""
    print(SPLASH_MSG)
    _ = input(
        WELCOME_MSG + "\n",
    )
