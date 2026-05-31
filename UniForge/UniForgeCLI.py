"""UniForge Engineering Assistant CLI - v1.1.5-beta"""

from awpc.src.unipy.uniflight.uniflight import *
from awpc.src.unipy.unispace.unispace import *
from awpc.src.unipy.unicrypt.unicrypt import *
from awpc.src.unipy.unipower.unipower import *
from awpc.src.unipy.unimath.unimath import *
from awpc.src.unipy.uniphys.mechanics import *
from awpc.src.unipy.unialgo.unialgo import *

from awpc.src.unipy import moduletools as mt

from awpc.src.unipy.uniCLI.uniCLI import (
    ExitEnvironmentSignal,
    clear_terminal, 
    dispatcher, 
    generate_completer,
    exit_env
)

from prompt_toolkit import prompt

MAINVER = "UniForge CLI v1.1.5-beta"
PIDVER = "v.0.0.1.alpha"
HOHMANNVER= "v.0.0.1.alpha"

### ENVIROMENTS 

def _mainEnv() -> None:
    clear_terminal()
    print(MAINVER)
    while True:        
        try:
            CommandString = prompt("UniForge >>> ", completer=MAINCOMPLETER)
            Result = dispatcher(CommandString, MAINCMDMAP, MAINARGMAP)
            clear_terminal()
            if Result is not None:
                print(Result)
            
        except Exception as e:
            print(f"[{x_color_text('ERROR', 'red')}] {type(e).__name__}: {e}")
def _pidEnv() -> None:
    clear_terminal()
    print(f"ORION PID Testing Environment {PIDVER}")
    while True:
        try:
            CommandString = prompt("PIDEnv >>> ", completer=PIDCOMPLETER)
            Result = dispatcher(CommandString, PIDCMDMAP, PIDARGMAP)
            if Result is not None:
                print(Result)    
        
        except ExitEnvironmentSignal:
            clear_terminal()
            print(f"ORION Environment {MAINVER}")
            break
        except Exception as e:
            print(f"[{x_color_text('ERROR', 'red')}] {type(e).__name__}: {e}")
def _hohmannEnv() -> None:
    clear_terminal()
    print(f"ORION Hohmann Calculation & Visualization Environment {HOHMANNVER}")
    while True:
        try:
            CommandString = prompt("HohmannENV >>> ", completer=HOHMANNCOMPLETER)
            Result = dispatcher(CommandString, HOHMANNCMDMAP, HOHMANNARGMAP)
            if Result is not None:
                print(Result)    
        
        except ExitEnvironmentSignal:
            clear_terminal()
            print(MAINVER)
            break
        except Exception as e:
            print(f"[{x_color_text('ERROR', 'red')}] {type(e).__name__}: {e}")

### MAPS

MAINARGMAP:    dict[str, dict[str, set]] = {
    "unipower":  mt.UNIPOWERARGMAP,
    "uniphys":   mt.UNIPHYSARGMAP,
    "uniflight": mt.UNIFLIGHTARGMAP,
    "unispace":  mt.UNISPACEARGMAP,
    "unimath":   mt.UNIMATHARGMAP,
    "unialgo":   mt.UNIALGOARGMAP,
    "unicrypt":  mt.UNICRYPTARGMAP,
    "enterenv": {
        "PIDEnv": {0},
        "HohmannEnv": {0},
    },
}
PIDARGMAP:     dict[str, dict[str, set]] = {
    "pidenv": {
        "exit": {0}
    }
}
HOHMANNARGMAP: dict[str, dict[str, set]] = {
    "hohmannenv": {
        "exit": {0}
    }
}

MAINCMDMAP:    dict[str, dict[str, callable]] = {
    "unipower":  mt.UNIPOWERCALLMAP,
    "uniphys":   mt.UNIPHYSCALLMAP,
    "uniflight": mt.UNIFLIGHTCALLMAP,
    "unispace":  mt.UNISPACECALLMAP,
    "unimath":   mt.UNIMATHCALLMAP,
    "unialgo":   mt.UNIALGOCALLMAP,
    "unicrypt":  mt.UNICRYPTCALLMAP,
    "enterenv": {
        "PIDEnv": _pidEnv,
        "HohmannEnv": _hohmannEnv,
    }
}
PIDCMDMAP:     dict[str, dict[str, callable]] = {
    "pidenv": {
        "exit": exit_env
    }
}
HOHMANNCMDMAP: dict[str, dict[str, callable]] = {
    "hohmannenv": {
        "exit": exit_env
    }
}

MAINCOMPLETER    = generate_completer(MAINCMDMAP)
PIDCOMPLETER     = generate_completer(PIDCMDMAP)
HOHMANNCOMPLETER = generate_completer(HOHMANNCMDMAP)

if __name__ == "__main__":
   _mainEnv()