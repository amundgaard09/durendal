"""
The `DuraPy` `Exceptions` module.

This module contains all the custom exceptions used in the `DuraPy` library.
"""

from ..types.color_dtypes import color_text

class ImpossibleTriangleError(Exception):
    """Raise when the sum of the angles of a triangle is not 180 degrees, a mathematical impossibility."""
    def __init__(self):
        super().__init__("The sum of the angles of a triangle can't be anything else than 180 degrees!")
class IncorrectArgumentCount(Exception):
    """Raises when the count of arguments given to a function is incorrect."""
    def __init__(self, Function: callable, GivenArgumentCount: int, WantedArgumentCount: set):
        super().__init__(f"Incorrect count of arguments for {color_text(Function.__name__, 'blue')}. {color_text(Function.__name__, 'blue')} takes {color_text(WantedArgumentCount, 'green')} but was given {color_text(GivenArgumentCount, 'red')}")
class InconsistencyError(Exception):
    """Raises when the VIR-values passed into PowerDissipation() gives inconsistent values for the three formulas."""
    def __init__(self, Function: callable, Inconsistency: str):
        super().__init__(f"Inconsistency error at {color_text(Function.__name__, 'blue')} with {color_text(Inconsistency, 'red')}")
class DimensionMismatch(Exception):
    """Raise when the dimensions of two units don't match when trying to convert or perform operations on them."""
    def __init__(self, string):
        super().__init__(string)
class InvalidColorCount(Exception):
    """Raised when the color count passed into a function of the resistor group is invalid."""
    def __init__(self, Function: callable):
        super().__init__(f"Invalid Color Count for {color_text(Function.__name__, 'blue')}")
class UnknownSubCommand(Exception):
    """Raises when an unknown subcommand gets caught in ValidateCommand()."""
    def __init__(self, Module: str, GivenCommand: str):
        super().__init__(f"Unknown command for {Module}: {color_text(GivenCommand, 'red')}")
class MissingSubCommand(Exception):
    """Raises when the subcommand is missing from a command string."""
    def __init__(self, module):
        super().__init__(f"Missing subcommand for {module}")    
class MissingParameters(Exception):
    """Raises when a function is not given enough / too many parameters."""
    def __init__(self, *args):
        super().__init__(*args)
class EmptyTokenList(Exception):
    """Raises when the TokenList passed into ValidateCommand() is empty."""
    def __init__(self):
        super().__init__(f"Empty TokenList! Make sure of correct tokens before verification attempt.")
class InvalidColors(Exception):
    """Raises when the colors passed into ResistorInsight() are invalid for the given band."""
    def __init__(self, Function: callable, IndexOfInvalidColors: int):
        super().__init__(f"Invalid colors for {color_text(Function.__name__, 'blue')} at indices {IndexOfInvalidColors}")
class UnknownModule(Exception):
    """Raises when an unknown module gets caught in ValidateCommand()."""
    def __init__(self, GivenModule: str):
        super().__init__(f"Unknown Module: {color_text(GivenModule, 'red')}") 
class InvalidInput(Exception):
    """Raises when an invalid input gets caught, e.g. a str for a wanted float."""
    def __init__(self, WantedType: type, GivenType: type):
        super().__init__(f"Invalid Input: WantedType: {color_text(WantedType, 'green')} GivenType: {color_text(GivenType, 'red')}") 





