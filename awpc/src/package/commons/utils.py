"""The `AWPC` utilities and dependencies module. This module contains all the dependencies of the `AWPC` library, such as custom exceptions, datatypes, and other utilities."""

ANSI_COLORS = {
    "black":  "\033[30m",
    "brown":  "\033[38;5;94m",
    "red":    "\033[31m",
    "orange": "\033[38;5;208m",
    "yellow": "\033[33m",
    "green":  "\033[32m",
    "blue":   "\033[34m",
    "violet": "\033[38;5;93m",
    "gray":   "\033[90m",
    "white":  "\033[97m",
    "gold":   "\033[38;5;178m",
    "silver": "\033[38;5;7m",
} 
"""The `ANSI` escape codes for the colors used in the `UNIx` library. The keys are the color names and the values are the corresponding `ANSI` escape codes."""

def xColorText(Text: str, Color: str) -> str:
    """Returns the given text in the given color using `ANSI` escape codes. If the color is not found, it returns the text without coloring."""
    Text = str(Text)
    ANSI = ANSI_COLORS.get(Color.lower(), '\033[0m')
    return ANSI + Text + '\033[0m'

