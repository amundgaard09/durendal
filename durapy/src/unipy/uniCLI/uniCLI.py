"""
The `AWPC` `UniPy` `UniCLI` module. 
This module contains the standard command-line interface framework from the `AWPC` library. 
It provides the necessary functions and classes to create a command-line interface for the `AWPC` library, 
including command parsing, argument validation, and command dispatching.
"""

import time
from prompt_toolkit.completion import NestedCompleter
from durapy.src.types.color_dtypes import color_text as color_text
from durapy.src.commons.exceptions import (
    IncorrectArgumentCount,
    EmptyTokenList, 
    MissingSubCommand, 
    UnknownSubCommand, 
    UnknownModule
)

import os, shlex, inspect

class ExitEnvironmentSignal(Exception):
    """Raise when the user wants to return to MAINEnv."""
    def __init__(self):
        super().__init__()
        
def exit_env() -> None:
    """Exit the current environment and return to MAINEnv."""
    raise ExitEnvironmentSignal

def generate_completer(Map: dict[str, dict]) -> NestedCompleter:
    """Generate a `NestedCompleter` dict with parameter names for each function."""
    
    CompleterDict = {}
    
    for Module, Subcommand in Map.items():
        CompleterDict[Module] = {}
        for SubcommandName, CommandFunction in Subcommand.items():
            Signature = inspect.signature(CommandFunction)
            CompleterDict[Module][SubcommandName] = {param: None for param in Signature.parameters}
    
    return NestedCompleter.from_nested_dict(CompleterDict)
def tokenize(RawCommandString: str) -> list[str]:
    """Tokenize a raw command string and return token list."""
    Tokens = shlex.split(RawCommandString)
    ProcessedTokens = []
    for Token in Tokens:
        if Token.startswith("[") and Token.endswith("]"):
            ProcessedValue = [float(x.strip()) for x in Token.strip("[]").split(",") if x.strip()]
            ProcessedTokens.append(ProcessedValue)
        else:
            ProcessedTokens.append(Token)
    return ProcessedTokens
def dispatcher(RawCommandString: str, CommandMap: dict[str, dict[str, callable]], ArgMap: dict[str, dict[str, set]]) -> callable:
    """The main dispatcher function that takes in a raw command string, tokenizes it, verifies the tokens, validates the arguments and dispatches the command to the correct function."""
    Tokens = tokenize(RawCommandString) 
    validate_command(Tokens, CommandMap, ArgMap)
    Module, Command, RawArgs = Tokens[0], Tokens[1], Tokens[2:]
    Args = []
    for arg in RawArgs:
        if arg == "_":
            Args.append(None)
        else:
            try:
                Args.append(float(arg))
            except ValueError:
                Args.append(arg)
            
    return CommandMap[Module][Command](*Args)
def validate_command(tokens: list, cmd_map: dict, arg_map: dict):
    if not tokens:
        raise EmptyTokenList

    module = tokens[0]
    if module not in cmd_map:
        raise UnknownModule(module)

    if len(tokens) < 2:
        raise MissingSubCommand(module)

    command = tokens[1]
    if command not in cmd_map[module]:
        raise UnknownSubCommand(module, command)

    args = tokens[2:]
    if len(args) not in arg_map[module][command]:
        raise IncorrectArgumentCount(cmd_map[module][command], len(args), arg_map[module][command])

def clear_terminal() -> None:
    os.system('cls' if os.name == 'nt' else 'clear')

def _console_msg(sender: str, sender_color: str, info: str, info_color: str = "white") -> str:
    return f"[{color_text(sender, sender_color)}] >>> {color_text(info, info_color)}"
def console_print(sender: str, sender_color: str, info: str, info_color: str = "white") -> None:
    print(_console_msg(sender, sender_color, info, info_color))
def console_input(sender: str, sender_color: str, prompt_info: str, prompt_color: str = "white") -> str | float:
    user_input = input(_console_msg(sender, sender_color, prompt_info, prompt_color) + " ")
    try:               return float(user_input)
    except ValueError: return user_input
def console_confirm(sender: str, sender_color: str, prompt_info: str, prompt_color: str = "white") -> bool:
    while True:
        user_input = input(_console_msg(sender, sender_color, prompt_info + ":", prompt_color) + " ").lower().strip()
        if user_input in ["y", "ye", "yes"]:
            return True
        elif user_input in ["n", "no"]:
            return False
        else:
            print(f"Please enter {color_text('y', 'green')} or {color_text('n', 'red')}")
