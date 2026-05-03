"""UniForge Engineering Assistant CLI - v1.1.5-beta"""

from awpc.unipy.uniflight.uniflight import *
from awpc.unipy.unispace.unispace import *
from awpc.unipy.unicrypt.unicrypt import *
from awpc.unipy.unipower.unipower import *
from awpc.unipy.unimath.unimath import *
from awpc.unipy.uniphys.uniphys import *
from awpc.unipy.unialgo.unialgo import *

from awpc.commons.utils import *
from awpc import moduleTools as mt

from awpc.unipy.uniCLI.uniCLI import (
    ExitEnvironmentSignal,
    clearTerminal, 
    Dispatcher, 
    GenerateCompleter,
    exitEnviroment
)

from prompt_toolkit import prompt

MAINVersion = "UniForge CLI v1.1.5-beta"
PIDVersion = "v.0.0.1.alpha"
HOHMANNVersion= "v.0.0.1.alpha"

### ENVIROMENTS 

def _mainEnv() -> None:
    clearTerminal()
    print(MAINVersion)
    while True:        
        try:
            CommandString = prompt("UniForge >>> ", completer=MAINCOMPLETER)
            Result = Dispatcher(CommandString, MAINCMDMAP, MAINARGMAP)
            clearTerminal()
            if Result is not None:
                print(Result)
            
        except Exception as e:
            print(f"[{xColorText('ERROR', 'red')}] {type(e).__name__}: {e}")
def _pidEnv() -> None:
    clearTerminal()
    print(f"ORION PID Testing Environment {PIDVersion}")
    while True:
        try:
            CommandString = prompt("PIDEnv >>> ", completer=PIDCOMPLETER)
            Result = Dispatcher(CommandString, PIDCMDMAP, PIDARGMAP)
            if Result is not None:
                print(Result)    
        
        except ExitEnvironmentSignal:
            clearTerminal()
            print(f"ORION Environment {MAINVersion}")
            break
        except Exception as e:
            print(f"[{xColorText('ERROR', 'red')}] {type(e).__name__}: {e}")
def _hohmannEnv() -> None:
    clearTerminal()
    print(f"ORION Hohmann Calculation & Visualization Environment {HOHMANNVersion}")
    while True:
        try:
            CommandString = prompt("HohmannENV >>> ", completer=HOHMANNCOMPLETER)
            Result = Dispatcher(CommandString, HOHMANNCMDMAP, HOHMANNARGMAP)
            if Result is not None:
                print(Result)    
        
        except ExitEnvironmentSignal:
            clearTerminal()
            print(MAINVersion)
            break
        except Exception as e:
            print(f"[{xColorText('ERROR', 'red')}] {type(e).__name__}: {e}")

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
        "exit": exitEnviroment
    }
}
HOHMANNCMDMAP: dict[str, dict[str, callable]] = {
    "hohmannenv": {
        "exit": exitEnviroment
    }
}

MAINCOMPLETER    = GenerateCompleter(MAINCMDMAP)
PIDCOMPLETER     = GenerateCompleter(PIDCMDMAP)
HOHMANNCOMPLETER = GenerateCompleter(HOHMANNCMDMAP)

if __name__ == "__main__":
   _mainEnv()