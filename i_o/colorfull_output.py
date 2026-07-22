from rich.console import Console
from rich.text import Text

from i_o.ascii_art import *  # Import the ASCII art from a separate file

test_massage_2 = """lorem ipsum dolor sit amet, consectetur adipiscing elit. Sed do eiusmod \ntempor incididunt ut labore et dolore magna aliqua. Ut enim ad minim \nveniam, quis nostrud exercitation ullamco laboris nisi ut aliquip ex ea \ncommodo consequat. Duis aute irure dolor in reprehenderit in \nvoluptate velit esse cillum dolore eu fugiat nulla pariatur. Excepteur \nsint occaecat cuplorem ipsum dolor sit amet, consectetur adipiscing elit. Sed do eiusmod \ntempor incididunt ut labore et dolore magna aliqua. Ut enim ad minim \nveniam, quis nostrud exercitation ullamco laboris nisi ut aliquip ex ea \ncommodo consequat. Duis aute irure dolor in reprehenderit in \nvoluptate velit esse cillum dolore eu fugiat nulla pariatur. Excepteur \nsint occaecat cupidatat non proident, lorem ipsum dolor sit amet, consectetur adipiscing elit. Sed do eiusmod \ntempor incididunt ut labore et dolore magna aliqua. Ut enim ad minim \nveniam, quis nostrud exercitation ullamco laboris nisi ut aliquip ex ea \ncommodo consequat. Duis aute irure dolor in reprehenderit in \nvoluptate velit esse cillum dolore eu fugiat nulla pariatur. Excepteur \nsint occaecat cupidatat non proident, idatat non proident, sunt in culpa qui officia deserunt mollit anim id\n est laborum."""
test_massage_3 = """l \nveniam, quis nostrud exercitation ullamco laboris nisi ut aliquip ex ea \ncommodo consequat. Duis aute irure dolor in reprehenderit in \nvoluptate velit esse cillum dolore eu fugiat nulla pariatur. Excepteur \nsint occaecat cupidatat non proident, idatat non proident, sunt in culpa qui officia deserunt mollit anim id\n est laborum."""


def output_colored_text(message: str, end="\n", flush=False):
    """Print massage text in a hartcodet blue color with rgb(60,37,205)
    color should be set to a constant value(later)
    """
    print(f"\033[38;2;90;117;225m{message}\033[0m", end=end, flush=flush)


def output_rainbow_text(message: str):
    """Print the given string with a colorful gradient effect.
    red is constant green and blue changed by index of line and character.
    can be modified and randomized to create different effects.(later)
    3 and 10 should be variable to change with line count(later)
    """
    console = Console()
    formatted_text = Text()

    lines = message.split("\n")
    factor = round(
        250 / len(lines),
    )  # Adjust the factor based on the number of lines

    for line_index, line in enumerate(lines):
        for char_index, char in enumerate(line):
            green = (char_index + 120) % 256
            red = 10
            blue = (line_index * factor) % 256

            style = f"rgb({red},{green},{blue})"
            formatted_text.append(char, style=style)

        formatted_text.append("\n")

    console.print(formatted_text)
