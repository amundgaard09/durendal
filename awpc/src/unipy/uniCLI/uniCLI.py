"""
The `AWPC` `UNIx` `UniCLI` module. 
This module contains the standard command-line interface framework from the `AWPC` library. 
It provides the necessary functions and classes to create a command-line interface for the `AWPC` library, 
including command parsing, argument validation, and command dispatching.
"""

import os, shlex, inspect

from prompt_toolkit.completion import NestedCompleter

from awpc.src.commons.exceptions import (
    IncorrectArgumentCount,
    EmptyTokenList, 
    MissingSubCommand, 
    UnknownSubCommand, 
    UnknownModule
)

class ExitEnvironmentSignal(Exception):
    """Raise when the user wants to return to MAINEnv."""
    def __init__(self):
        super().__init__()

def exitEnviroment() -> None:
    """Exit the current environment and return to MAINEnv."""
    raise ExitEnvironmentSignal

def GenerateCompleter(Map: dict[str, dict]) -> NestedCompleter:
    """Generate a `NestedCompleter` dict with parameter names for each function."""
    
    CompleterDict = {}
    
    for Module, Subcommand in Map.items():
        CompleterDict[Module] = {}
        for SubcommandName, CommandFunction in Subcommand.items():
            Signature = inspect.signature(CommandFunction)
            CompleterDict[Module][SubcommandName] = {param: None for param in Signature.parameters}
    
    return NestedCompleter.from_nested_dict(CompleterDict)
def Tokenize(RawCommandString: str) -> list[str]:
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
def Dispatcher(RawCommandString: str, CommandMap: dict[str, dict[str, callable]], ArgMap: dict[str, dict[str, set]]) -> callable:
    """The main dispatcher function that takes in a raw command string, tokenizes it, verifies the tokens, validates the arguments and dispatches the command to the correct function."""
    Tokens = Tokenize(RawCommandString) 
    ValidateCommand(Tokens, CommandMap, ArgMap)
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
def ValidateCommand(tokens: list, cmd_map: dict, arg_map: dict):
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

def clearTerminal() -> None:
    os.system('cls' if os.name == 'nt' else 'clear')
