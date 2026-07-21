from ascii_art import *  # Import the ASCII art from a separate file
from rich.console import Console
from rich.text import Text

message = pirat_ascii  # Replace with your desired message
console = Console()


def output_colored(message: str) -> str:
    """Print the given string with a colorful gradient effect.
    red is constant green and blue changed by index of line and character.
    can be modified and randomized to create different effects.(later)
    3 and 10 should be variable to change with line count(later)
    """
    formatted_text = Text()

    lines = message.split("\n")

    for line_index, line in enumerate(lines):
        for char_index, char in enumerate(line):
            green = (char_index * 3) % 256
            red = 10
            blue = (line_index * 10) % 256

            style = f"rgb({red},{green},{blue})"
            formatted_text.append(char, style=style)

        formatted_text.append("\n")

    # console.print(formatted_text)
    return formatted_text  # Return the formatted text instead of printing it


console.print(output_colored(message))
