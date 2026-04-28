"""UniForge Engineering Assistant CLI - v1.1.5-beta"""

import math

from awpc.unimath.unimath import *
from awpc.unicrypt.unicrypt import *
from awpc.unipower.unipower import *
from awpc.uniphys.uniphys import *

from awpc.uniCLI.uniCLI import clearTerminal, Dispatcher, GenerateCompleter, ExitEnvironmentSignal
from awpc.utils.utils import *
from awpc import moduleTools as mt

from prompt_toolkit import prompt

MAINVersion = "UniForge CLI v1.1.5-beta"
PIDVersion = "v.0.0.1.alpha"
HOHMANNVersion= "v.0.0.1.alpha"

### SYSTEM

def _exitEnviroment() -> None:
    """Exit the current environment and return to MAINEnv."""
    raise ExitEnvironmentSignal

### UNICON

def PIDStep(CurrentError: float, TimeInterval: float, Kp: float, Ki: float, Kd: float, LastError: float | None = 0, Integral: float | None = 0) -> str:
# THIS CODE IS UNUSED UNTIL FURTHER NOTICE!
    P = Kp * CurrentError

    I = Integral + Ki * CurrentError * TimeInterval

    D = Kd * (CurrentError - LastError) / TimeInterval

    return f"Sum: {P+I+D} - P: {P} - I: {I} - D: {D}"
 
### UNIFLIGHT

def T2WRatio(Thrust: float, Weight: float) -> str:
    """Thrust to Weight ratio calculator. Ensure consistent units!"""
    Ratio = Thrust / Weight
    return f"Ratio: {xColorText(f'{Ratio}', 'green' if Ratio > 1 else 'red' if Ratio != 1 else 'yellow')}" 
def MachNumber(Velocity: float, SpeedOfSound: float | None = MACH) -> str:
    """Mach Number Calulator. Speed of sound is defaulted to 343 m/s. Ensure consistent units!"""
    mach = Velocity / SpeedOfSound
    label = ('SUBSONIC' if mach < 1 else 'TRANSONIC' if abs(mach - 1) < 0.01 else 'SUPERSONIC' if mach < 5 else 'HYPERSONIC' if mach < 10 else 'HIGH-HYPERSONIC')
    color = ('red' if mach < 1 else 'yellow' if mach == 1 else 'green' if mach < 5 else 'blue' if mach < 10 else 'violet')
    return f"Ratio: {xColorText(f'{mach} - {label}', color)}"
                                
def DynamicPressure(Velocity: float, AirDensity: float | None = 1.225) -> Quantity:
    return Quantity(0.5 * Velocity ** 2 * AirDensity, UNITS["Pa"])

def LiftEquation(LiftCoefficient: float, DynamicPressure: float, ReferenceArea: float) -> Quantity:
    return Quantity(LiftCoefficient * DynamicPressure * ReferenceArea, UNITS["N"])
def DragEquation(DragCoefficient: float, DynamicPressure: float, ReferenceArea: float) -> Quantity:
    return Quantity(DragCoefficient * DynamicPressure * ReferenceArea, UNITS["N"])

### UNISPACE - NOTE Hohmann transfer delta-v + visualization env - COMING SOON

def OrbitalPeriod(SemiMajorAxis: float, M: float, m: float) -> Quantity:
    return Quantity((2 * math.pi * math.sqrt(SemiMajorAxis ** 3 / (G * (M + m)))), UNITS["S"])
def OrbitalVelocity(OrbitalRadius: float = EARTH_R, Mass: float = EARTH_M) -> Quantity:
    return Quantity((math.sqrt((G * Mass) / OrbitalRadius)), UNITS["m/s"])
def EscapeVelocity(Radius: float = EARTH_R, Mass: float = EARTH_M) -> Quantity:
    return Quantity((math.sqrt(2) * OrbitalVelocity(Radius, Mass)), UNITS["m/s"])

def GravitationalForce(Mass1: float, Mass2: float, Distance: float) -> Quantity:
    return Quantity((G * Mass1 * Mass2 / Distance ** 2), UNITS["N"])
def SurfaceGravity(Mass: float, Radius: float) -> Quantity:
    return Quantity((G * Mass / Radius ** 2), UNITS["m/s^2"])

def EinsteinMassEnergyEquivalence(Mass: float) -> Quantity:
    return Quantity((Mass * C ** 2), UNITS["J"])
def TsiolkovskyRocketEquation(ExhaustVelocity: float, InitialMass: float, FinalMass: float) -> Quantity:
    return Quantity((ExhaustVelocity * math.log(InitialMass / FinalMass)), UNITS["Δv"])

### UNIALGO

def FibonacciList(ListLength: float) -> list[int]:
    """Fibonacci sequence generator that returns a list of the sequence up to the given length."""
    
    try:
        ListLength = int(ListLength)  
    except ValueError:
        raise ValueError("FibonacciInteger does not take floats or strings!")      
    
    fib0, fib1 = 0, 1
    FiboList = [fib0, fib1]
    
    if ListLength < 2:
        raise ValueError("FibonacciList does not take integers less than 2!")
    
    for _ in range(0, (ListLength - 2)):
        fib2 = fib0 + fib1
        fib0, fib1 = fib1, fib2
        FiboList.append(fib2)
        
    return FiboList   
def FibonacciInteger(FiboIndex: float) -> int:
    """Fibonacci integer generator that returns the Fibonacci integer at the given index.""" 
    
    try:
        FiboIndex = int(FiboIndex)  
    except ValueError:
        raise ValueError("FibonacciInteger does not take floats or strings!") 
    
    if FiboIndex < 2:
        raise ValueError("FibonacciInteger does not take integers less than 2!")
    
    if FiboIndex == 2:
        return 1  
      
    fib0, fib1, fib2 = 0, 1, 1
    
    for _ in range(0, (FiboIndex - 2)):
        fib2 = fib0 + fib1
        fib0, fib1 = fib1, fib2
        
    return fib2

def LovelacesAlgorithm(a: float, b: float, c: float, d: float, e: float, f: float) -> tuple:
    """Lovelace's algorithm for solving systems of linear equations."""
    if a*e == b*d: 
        raise ValueError("The system has no unique solution.")
    
    Dx = c*e - b*f
    Dy = a*f - c*d
    x = Dx / (a*e - b*d)
    y = Dy / (a*e - b*d)
    return (x, y)

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
    "unipower": {
        "ohmslaw": {2, 3},
        "voltdivider": {3},
        "rctimeconstant": {2},
        "inductorimpedance": {2},
        "powerdissipation": {2, 3},
        "resistorinsight": {4, 5},
        "resistorviz": {4, 5},
        "totalcapacitance": {2},
        "totalesr": {2},
    },
    "uniphys": mt.UNIPHYSARGMAP,
    "uniflight": {
        "T2Wratio": {2},
        "machnumber": {1, 2},
        "dynamicpressure": {1, 2},
        "liftequation": {3},
        "dragequation": {3},
    },
    "unispace": {
        "tsiolkovskyrocketequation": {3},
        "orbitalvelocity": {0, 1, 2},
        "escapevelocity": {0, 1, 2},
        "gravitationalforce": {3},
        "surfacegravity": {2},
        "orbitalperiod": {3},
        "einsteinmassenergyequivalence": {1},
    },
    "unimath": mt.UNIMATHARGMAP,
    "unialgo": {
        "fibonaccilist": {1},
        "fibonacciinteger": {1},
        "lovelacesalgorithm": {6},
    },
    "unicrypt": mt.UNICRYPTARGMAP,
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
    "unipower": {
        "ohmslaw": OhmsLaw,
        "voltdivider": VoltDivider,
        "rctimeconstant": RCTimeConstant,
        "inductorimpedance": InductorImpedance,
        "powerdissipation": PowerDissipation,
        "resistorinsight": ResistorInsight,
        "resistorviz": ResistorViz,
        "totalcapacitance": TotalCapacitance,
        "totalesr": TotalESR,
    },
    "uniphys": mt.UNIPHYSCALLMAP,
    "uniflight": {
        "T2Wratio": T2WRatio,
        "machnumber": MachNumber,
        "dynamicpressure": DynamicPressure,
        "liftequation": LiftEquation,
        "dragequation": DragEquation,
    },
    "unispace": {
        "tsiolkovskyrocketequation": TsiolkovskyRocketEquation,
        "orbitalvelocity": OrbitalVelocity,
        "escapevelocity": EscapeVelocity,
        "gravitationalforce": GravitationalForce,
        "surfacegravity": SurfaceGravity,
        "orbitalperiod": OrbitalPeriod,
        "einsteinmassenergyequivalence": EinsteinMassEnergyEquivalence,
    },
    "unimath": mt.UNIMATHCALLMAP,
    "unialgo": {
        "fibonaccilist": FibonacciList,
        "fibonacciinteger": FibonacciInteger,
        "lovelacesalgorithm": LovelacesAlgorithm,
    },
    "unicrypt":  mt.UNICRYPTCALLMAP,
    "enterenv": {
        "PIDEnv": _pidEnv,
        "HohmannEnv": _hohmannEnv,
    }
}
PIDCMDMAP:     dict[str, dict[str, callable]] = {
    "pidenv": {
        "exit": _exitEnviroment
    }
}
HOHMANNCMDMAP: dict[str, dict[str, callable]] = {
    "hohmannenv": {
        "exit": _exitEnviroment
    }
}

MAINCOMPLETER    = GenerateCompleter(MAINCMDMAP)
PIDCOMPLETER     = GenerateCompleter(PIDCMDMAP)
HOHMANNCOMPLETER = GenerateCompleter(HOHMANNCMDMAP)

if __name__ == "__main__":
   _mainEnv()