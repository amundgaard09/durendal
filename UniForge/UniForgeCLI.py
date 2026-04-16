"""UniForge Engineering Assistant CLI - v1.1.4-beta"""

import os, math, json, numpy, shlex, inspect

from awpc.unimath.unimath import *
from awpc.unicrypt.unicrypt import *
from awpc.utils.utils import *

from prompt_toolkit import prompt
from prompt_toolkit.completion import NestedCompleter

MAINVersion = f"UniForge CLI v1.1.4-beta"
PIDVersion = f"v.0.0.1.alpha"
HOHMANNVersion= f"v.0.0.1.alpha"

### CONSTANTS

BANDS = {
    "black":  0,
    "brown":  1,
    "red":    2,
    "orange": 3,
    "yellow": 4,
    "green":  5,
    "blue":   6,
    "violet": 7,
    "gray":   8,
    "white":  9,
}
MULTIPLIERS = {
    "black":  1,
    "brown":  10,
    "red":    1e2,
    "orange": 1e3,
    "yellow": 1e4,
    "green":  1e5,
    "blue":   1e6,
    "violet": 1e7,
    "gray":   1e8,
    "white":  1e9,
    "gold":   0.1,
    "silver": 0.01,
}
TOLERANCES = {
    "brown":  1,
    "red":    2,
    "green":  0.5,
    "blue":   0.25,
    "violet": 0.1,
    "gray":   0.05,
    "gold":   5,
    "silver": 10,
}

### ERRORS

class InvalidColorCount(Exception):
    """Raised when the color count passed into a function of the resistor group is invalid."""
    def __init__(self, Function: callable):
        super().__init__(f"Invalid Color Count for {ColorText(Function.__name__, 'blue')}")
class InconsistencyError(Exception):
    """Raises when the VIR-values passed into PowerDissipation() gives inconsistent values for the three formulas."""
    def __init__(self, Function: callable, Inconsistency: str):
        super().__init__(f"Inconsistency error at {ColorText(Function.__name__, 'blue')} with {ColorText(Inconsistency, 'red')}")
class IncorrectArgumentCount(Exception):
    """Raises when the count of arguments given to a function is incorrect."""
    def __init__(self, Function: callable, GivenArgumentCount: int, WantedArgumentCount: set):
        super().__init__(f"Incorrect count of arguments for {ColorText(Function.__name__, 'blue')}. {ColorText(Function.__name__, 'blue')} takes {ColorText(WantedArgumentCount, 'green')} but was given {ColorText(GivenArgumentCount, 'red')}")
class InvalidColors(Exception):
    """Raises when the colors passed into ResistorInsight() are invalid for the given band."""
    def __init__(self, Function: callable, IndexOfInvalidColors: int):
        super().__init__(f"Invalid colors for {ColorText(Function.__name__, 'blue')} at indices {IndexOfInvalidColors}")
class UnknownModule(Exception):
    """Raises when an unknown module gets caught in VerifyTokens()."""
    def __init__(self, GivenModule: str):
        super().__init__(f"Unknown Module: {ColorText(GivenModule, 'red')}") 
class UnknownSubCommand(Exception):
    """Raises when an unknown subcommand gets caught in VerifyTokens()."""
    def __init__(self, Module: str, GivenCommand: str):
        super().__init__(f"Unknown command for {Module}: {ColorText(GivenCommand, 'red')}")
class MissingSubCommand(Exception):
    """Raises when the subcommand is missing from a command string."""
    def __init__(self, module):
        super().__init__(f"Missing subcommand for {module}")    
class MissingParameters(Exception):
    """Raises when a function is not given enough parameters."""
    def __init__(self, Function: callable, MissingParameters: list):
        super().__init__(f"Missing parameter {ColorText(MissingParameters, 'red')} for {ColorText(Function.__name__, 'blue')}.")
class EmptyTokenList(Exception):
    """Raises when the TokenList passed into VerifyTokens() is empty."""
    def __init__(self):
        super().__init__(f"Empty TokenList! Make sure of correct tokens before verification attempt.")

### SIGNALS

class ExitEnvironmentSignal(Exception):
    """Raise when the user wants to return to MAINEnv."""
    def __init__(self):
        super().__init__()
    
### UTILS

def InsertJSON(PathToJSON: str, ContentDict: dict) -> None:
    """Inserts a dictionary into a JSON file. If the file does not exist, it creates it. Returns True if the operation was successful, False otherwise."""
    with open(PathToJSON, 'w') as JSONFile:
        json.dump(ContentDict, JSONFile, indent=4, sort_keys=True)
def ExtractJSON(PathToJSON: str) -> dict:
    """Extracts a JSON file and returns the content as a dictionary. Returns None if the file is not found or if there is an error during extraction."""
    try:
        with open(PathToJSON, 'r', encoding='utf-8') as file:
            return json.load(file)
    except Exception:
        return None
def CLIConvert(Value: float, FromUnit: str, ToUnit: str) -> Quantity:
    return Convert(Quantity(Value, UNITS[FromUnit]), UNITS[ToUnit])

### SYSTEM

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
    VerifyTokens(Tokens, CommandMap)
    ValidateArgs(Tokens, CommandMap, ArgMap)
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
def VerifyTokens(TokenList: list, CommandMap: dict) -> bool:
    """Verify validity of tokens before dispatching."""
    if not TokenList: 
        raise EmptyTokenList
    elif TokenList[0] not in CommandMap:
        raise UnknownModule(TokenList[0])
    elif len(TokenList) < 2:
        raise MissingSubCommand(TokenList[0])
    elif TokenList[1] not in CommandMap[TokenList[0]]:
        raise UnknownSubCommand(TokenList[0], TokenList[1])
    else:
        return True
def ValidateArgs(TokenList: list, CommandMap: dict, ArgMap: dict) -> bool:
    """Validate that the arguments passed into a function are of the correct length."""
    Module, Command, Args = TokenList[0], TokenList[1], TokenList[2:]
    if len(Args) not in ArgMap[Module][Command]:
        raise IncorrectArgumentCount(CommandMap[Module][Command], len(Args), ArgMap[Module][Command])
    else:
        return True 

def _exitEnviroment() -> None:
    """Exit the current environment and return to MAINEnv."""
    raise ExitEnvironmentSignal
def _clearTerminal() -> None:
    os.system('cls' if os.name == 'nt' else 'clear')

### UNIPOWER

def OhmsLaw(V: float | None = None, I: float | None = None, R: float | None = None) -> str:
    """Ohms Law calculation for Voltage, Current, and Resistivity.
    V = I * R
    I = V / R
    R = V / I
    """
    
    if V is not None: V = float(V)
    if I is not None: I = float(I)
    if R is not None: R = float(R)
            
    if (V, I, R).count(None) > 1:
        MissingParams = []
        for idx, value in enumerate((V, I, R)):
            if value is None:
                MissingParams.append(("V", "I", "R")[idx])
        
        raise MissingParameters(OhmsLaw, MissingParams)
    
    if V is None:
        V = I * R
    elif I is None:
        I = V / R
    elif R is None:
        R = V / I
        
    return f"V: {V}, I: {I}, R: {R}"
def VoltDivider(VIn: float, R1: float, R2: float) -> Quantity:
    """Calculates the output voltage of a voltage divider from input voltage and the two resistances."""
    return Quantity((VIn * (R2 / (R1 + R2))), UNITS["V"])
def RCTimeConstant(Capacitance: float, Resistance: float) -> Quantity:
    """Calculates the time constant of an RC circuit from capacitance in farads and resistance in ohms."""
    return Quantity((Capacitance * Resistance), UNITS["S"])
def InductorImpedance(Hertz: float, Inductance: float) -> Quantity:
    """Calculates the impedance of an inductor at a given frequency in hertz and inductance in henrys."""
    return Quantity((2 * numpy.pi * Hertz * Inductance), UNITS["Ohm"])
def PowerDissipation(V: float | None = None, I: float | None = None, R: float | None = None) -> Quantity:
    """Calculates power dissipation from voltage, current and resistance. If all three parameters are given, it checks for consistency between the three formulas P = I^2 * R, P = V^2 / R and P = V * I."""
    if (V, I, R).count(None) > 1:
        MissingParams = []
        for idx, value in enumerate((V, I, R)):
            if value is None:
                MissingParams.append(("V", "I", "R")[idx])
        
        raise MissingParameters(PowerDissipation, MissingParams)

    if (V, I, R).count(None) == 1:
        if V is None:
            P = I ** 2 * R
        elif I is None:
            P = V ** 2 / R
        elif R is None:
            P = V * I
        return Quantity(P, UNITS["W"])
    
    else:
        P1 = I ** 2 * R
        P2 = V ** 2 / R
        P3 = V * I
        
        if math.isclose(P1, P2):
            if math.isclose(P2, P3):
                return Quantity(((P1 + P2 + P3) / 3), UNITS["W"])
            else:
                raise InconsistencyError(PowerDissipation, "Inconsistency with P3 = V * I")
        else:
            if math.isclose(P1, P3):
                raise InconsistencyError(PowerDissipation, "Inconsistency with P2 = V ** 2 / R")
            else:
                raise InconsistencyError(PowerDissipation, "Inconsistency with P1 = I ** 2 * R")
    
def ResistorViz(C1: str, C2: str, C3: str, C4: str, C5: str | None = None) -> str:
    """Prints a ASCII representation of a resistor with the color code""" 
    def color_block(color: str):
        ansi = ANSI_COLORS.get(color.lower(), "\033[0m")
        reset = "\033[0m"
        return f"{ansi}    {reset}"
    if C5 is not None:
        return f"    <----------------------------->\n    |                             |\n    |  ┌────┬────┬────┬────┬────┐ |\n   ----│{color_block(C1)}│{color_block(C2)}│{color_block(C3)}│{color_block(C4)}│{color_block(C5)}|----\n    |  └────┴────┴────┴────┴────┘ |\n    |                             |\n    <----------------------------->" 
    else:
        return f"    <------------------------->\n    |                         |\n    |  ┌────┬────┬────┬────┐  |\n   ----│{color_block(C1)}│{color_block(C2)}│{color_block(C3)}│{color_block(C4)}│----\n    |  └────┴────┴────┴────┘  |\n    |                         |\n    <------------------------->" 
def ResistorInsight(C1: str, C2: str, C3: str, C4: str, C5: str | None = None) -> tuple:
    """Takes in 4/5 colors of a resistor and returns the resistivity and tolerance range."""
    
    Band1 = BANDS.get(C1)
    Band2 = BANDS.get(C2)
    
    if C5 is None:
        Multiplier = MULTIPLIERS.get(C3)
        Tolerance = TOLERANCES.get(C4)
        bands = (Band1, Band2, Multiplier, Tolerance)
        
        if None in bands:
            raise InvalidColors(ResistorInsight, bands.index(None) + 1)
        
        Ohms = (Band1 * 10 + Band2) * Multiplier
        
    else:
        Band3 = BANDS.get(C3)
        Multiplier = MULTIPLIERS.get(C4)
        Tolerance = TOLERANCES.get(C5)
        bands = (Band1, Band2, Band3, Multiplier, Tolerance)
        
        if None in bands:
            raise InvalidColors(ResistorInsight, bands.index(None) + 1)
        
        Ohms = (Band1 * 100 + Band2 * 10 + Band3) * Multiplier

    ToleranceDecimal = Tolerance / 100
    LowerBound = Ohms * (1 - ToleranceDecimal)
    UpperBound = Ohms * (1 + ToleranceDecimal)
    
    ResistanceString = f"Resistance: {Ohms}Ω"
    RangeString = f"Range: {LowerBound}Ω - {UpperBound}Ω ( {Tolerance}% )"

    return (ResistanceString, RangeString)

### TODO finish wrapping these functions
def TotalESR(caps: list[tuple], ConnectionType: Literal["parallel", "series"]) -> float:
    """Calculates total ESR of a list of capacitors based on their connection type. Caps are in the format (capacitance, voltage, esr) for now."""
    if ConnectionType == "series":
        return sum(cap[2] for cap in caps)
    elif ConnectionType == "parallel":
        try:
            return 1 / sum(1 / cap[2] for cap in caps if cap[2] != 0)
        except ZeroDivisionError:
            return 0  
    else:
        raise ValueError("Connection type must be 'parallel' or 'series'")
def TotalCapacitance(caps: list[tuple], ConnectionType: Literal["parallel", "series"]) -> str: ### caps (capacitance, voltage, esr) (for now)
    """Calculates total capacitance, voltage limit and ESR of a list of capacitors based on their connection type."""
        
    if ConnectionType == "parallel":
        totalCapacitance = 0
        for cap in caps:
            totalCapacitance += cap[0]
        VoltLimit = min([cap[1] for cap in caps])
        
    elif ConnectionType == "series":
        RawTotalCapacitance = 0
        for cap in caps:
            RawTotalCapacitance += ((cap[0])**(-1))
        totalCapacitance = RawTotalCapacitance**(-1)
        VoltLimit = sum([cap[1] for cap in caps])   
    else:
        raise ValueError("Connection type must be 'parallel' or 'series'")

    return f"Total Capacitance: {totalCapacitance}, Volt Limit: {VoltLimit}, Total ESR: {TotalESR(caps, ConnectionType)}"

### UNIMAKE

def Torque(MomentArmDistance: float, Force: float) -> Quantity:
    """Returns torque in newtons from moment arm distance and force."""
    return Quantity((MomentArmDistance * Force), UNITS["Nm"])
def GearRatio(DrivingGearTeethCount: int, DrivenGearTeethCount: int) -> str:
    """Returns the gear ratio from the driving gear's teeth count and the driven gear's teeth count."""
    Ratio = DrivenGearTeethCount / DrivingGearTeethCount
    if Ratio > 1:
        return f"{Ratio} - {ColorText('Speed-', 'red')} - {ColorText('Torque+', 'green')}"
    elif Ratio < 1:
        return f"{Ratio} - {ColorText('Speed+', 'green')} - {ColorText('Torque-', 'red')}"
    else:
        return f"{Ratio} - Same Speed - Same Torque"
def AngularVelocityR(RPM: float) -> Quantity:
    """Returns angular velocity from RPM in radians/s"""
    return Quantity((RPM * math.pi / 30), UNITS["Rad"])
def AngularVelocityD(RPM: float) -> Quantity:
    """Returns angular velocity from RPM in degrees/s"""
    return Quantity(R2D((RPM * math.pi / 30)), UNITS["Deg"])

def KineticEnergy(Mass: float, Velocity: float) -> Quantity:
    """Returns the kinetic energy from mass in kgs and velocity in m/s"""
    return Quantity((0.5 * Mass * Velocity**2), UNITS["J"])
def PotentialEnergy(Mass: float, Height: float, Gravity: float | None = EARTH_G) -> Quantity:
    """Returns the potential energy of a mass. Gravity is defaulted to 9.8m /s^2"""
    return Quantity(Mass * Gravity * Height, UNITS["J"])

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
    return f"Ratio: {ColorText(f'{Ratio}', 'green' if Ratio > 1 else 'red')}" if Ratio != 1 else f"Ratio: {ColorText(f'{Ratio}', 'yellow')}"
def MachNumber(Velocity: float, SpeedOfSound: float | None = SPEED_SOUND) -> str:
    """Mach Number Calulator. Speed of sound is defaulted to 343 m/s. Ensure consistent units!"""
    MachNumber = Velocity / SpeedOfSound
    return (f"Ratio: {ColorText(f'{MachNumber} - SUPERSONIC', 'green') if MachNumber > 1 else ColorText(f'{MachNumber} - SUBSONIC', 'red')}" if MachNumber != 1 else f"Ratio: {ColorText(f'{MachNumber} - TRANSONIC', 'yellow')}") if MachNumber < 5 else f"Ratio: {ColorText(f'{MachNumber} - HYPERSONIC', 'blue')}"
def DynamicPressure(Velocity: float, AirDensity: float | None = 1.225) -> Quantity:
    return Quantity(0.5 * Velocity ** 2 * AirDensity, UNITS["Pa"])

def LiftEquation(LiftCoefficient: float, DynamicPressure: float, ReferenceArea: float) -> Quantity:
    return Quantity(LiftCoefficient * DynamicPressure * ReferenceArea, UNITS["N"])
def DragEquation(DragCoefficient: float, DynamicPressure: float, ReferenceArea: float) -> Quantity:
    return Quantity(DragCoefficient * DynamicPressure * ReferenceArea, UNITS["N"])

### UNISPACE - Hohmann transfer delta-v + visualization env - COMING SOON

def OrbitalPeriod(SemiMajorAxis: float, M: float, m: float) -> Quantity:
    return Quantity((2 * math.pi * math.sqrt(SemiMajorAxis ** 3 / (G * (M + m)))), UNITS["S"])
def OrbitalVelocity(OrbitalRadius: float = EARTH_R, Mass: float = EARTH_M) -> Quantity:
    return Quantity((math.sqrt((G*Mass) / OrbitalRadius)), UNITS["m/s"])
def EscapeVelocity(Radius: float = EARTH_R, Mass: float = EARTH_M) -> Quantity:
    return Quantity((math.sqrt(2) * OrbitalVelocity(Radius, Mass).value), UNITS["m/s"])

def GravitationalForce(Mass1: float, Mass2: float, Distance: float) -> Quantity:
    return Quantity((G * Mass1 * Mass2 / Distance ** 2), UNITS["N"])
def SurfaceGravity(Mass: float, Radius: float) -> Quantity:
    return Quantity((G * Mass / Radius ** 2), UNITS["m/s^2"])

def EinsteinMassEnergyEquivalence(Mass: float) -> Quantity:
    return Quantity((Mass * C ** 2), UNITS["J"])
def TsiolkovskyRocketEquation(ExhaustVelocity: float, InitialMass: float, Finalmass: float) -> Quantity:
    return Quantity((ExhaustVelocity * math.log(InitialMass/Finalmass)), UNITS["Δv"])

### UNIALGO

def FibonacciList(ListLength: float) -> list[int]:
    """Fibonacci sequence generator that returns a list of the sequence up to the given length."""
    
    try:
        ListLength = int(ListLength)  
    except ValueError:
        raise ValueError("FibonacciInteger does not take floats or strings!")      
    
    fib0, fib1 = 0, 1
    FiboList = [fib0, fib1]
    
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
    """Lovelace's algorithm for solving systems of linear equations"""
    if (a*e - b*d) == 0:
        raise ValueError("The system has no unique solution.")
    
    Dx = c*e - b*f
    Dy = a*f - c*d
    x = Dx / (a*e - b*d)
    y = Dy / (a*e - b*d)
    return (x, y)

### ENVIROMENTS 

def _mainEnv() -> None:
    _clearTerminal()
    print(MAINVersion)
    while True:        
        try:
            CommandString = prompt("UniForge >>> ", completer=MAINCOMPLETER)
            Result = Dispatcher(CommandString, MAINCMDMAP, MAINARGMAP)
            if Result is not None:
                print(Result)
            
        except Exception as e:
            print(e.__str__())
def _pidEnv() -> None:
    _clearTerminal()
    print(f"ORION PID Testing Environment {PIDVersion}")
    while True:
        try:
            CommandString = prompt("PIDEnv >>> ", completer=PIDCOMPLETER)
            Result = Dispatcher(CommandString, PIDCMDMAP, PIDARGMAP)
            if Result is not None:
                print(Result)    
        
        except ExitEnvironmentSignal:
            _clearTerminal()
            print(f"ORION Environment {MAINVersion}")
            break
        except Exception as e:
            print(e.__str__())
def _hohmannEnv() -> None:
    _clearTerminal()
    print(f"ORION Hohmann Calculation & Visualization Environment {HOHMANNVersion}")
    while True:
        try:
            CommandString = prompt("HohmannENV >>> ", completer=HOHMANNCOMPLETER)
            Result = Dispatcher(CommandString, HOHMANNCMDMAP, HOHMANNARGMAP)
            if Result is not None:
                print(Result)    
        
        except ExitEnvironmentSignal:
            _clearTerminal()
            print(MAINVersion)
            break
        except Exception as e:
            print(e.__str__())

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
    "unimake": {
        "torque": {2},
        "gearratio": {2},
        "angularvelocityr": {1},
        "angularvelocityd": {1},
        "kineticenergy": {2},
        "potentialenergy": {2, 3},
    },
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
    "unimath": {
        "triextrapolate": {4, 6},
        "quadratic": {3},
        "pythagoras": {2, 3},
        "D2R": {1},
        "R2D": {1},
        "sinerule": {7},
        "cosinerule": {3},
        "reversecosinerule": {3},
        "sasarea": {3},
        "herons": {3},
        "slope": {4},
        "linefrompoints": {4},
        "linearzero": {2},
        "quadraticvertex": {3},
        "quadraticnumroots": {3},
        "cubicevaluation" : {5},
        "evaluatequadratic": {4},
        "lineintersection": {4},
        "distance": {4},
        "derivative": {1, 2},
        "tangentformula": {2},
        "convert": {3},
    },
    "unialgo": {
        "fibonaccilist": {1},
        "fibonacciinteger": {1},
        "lovelacesalgorithm": {6},
    },
    "unicrypt": {
        "binaryencrypt": {1},
        "binarydecrypt": {1},
        "ceasarencrypt": {2},
        "ceasardecrypt": {2},
        "vigenereencrypt": {2},
        "vigeneredecrypt": {2},
        "railfenceencrypt": {2},
        "railfencedecrypt": {2},
        "otpencrypt": {2},
        "otpdecrypt": {2},
    },
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
    "unimake": {
        "torque": Torque,
        "gearratio": GearRatio,
        "angularvelocityr": AngularVelocityR,
        "angularvelocityd": AngularVelocityD,
        "kineticenergy": KineticEnergy,
        "potentialenergy": PotentialEnergy,
    },
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
    "unimath": {
        "triextrapolate": TriExtrapolate,
        "pythagoras": Pythagoras,
        "D2R": D2R,
        "R2D": R2D,
        "sinerule": SineRule,
        "cosinerule": CosineRule,
        "reversecosinerule": ReverseCosineRule,
        "sasarea": SASArea,
        "herons": HeronsFormula,
        "slope": Slope,
        "linefrompoints": LineFromPoints,
        "linearzero": LinearZero,
        "quadraticsolutions": QuadraticSolutions,
        "quadraticvertex": QuadraticVertex,
        "quadraticnumroots": QuadraticNumRoots,
        "quadraticevaluation": QuadraticEvaluation,
        "cubicevaluation" : CubicEvaluation,
        "lineintersection": LineIntersection,
        "distance": Distance,
        "derivative": Derivative,
        "tangentformula": TangentFormula,
        "convert": CLIConvert,
    },
    "unialgo": {
        "fibonaccilist": FibonacciList,
        "fibonacciinteger": FibonacciInteger,
        "lovelacesalgorithm": LovelacesAlgorithm,
    },
    "unicrypt": {
        "binaryencrypt": BinaryEncrypt,
        "binarydecrypt": BinaryDecrypt,
        "ceasarencrypt": CeasarEncrypt,
        "ceasardecrypt": CeasarDecrypt,
        "vigenereencrypt": VigenereEncrypt,
        "vigeneredecrypt": VigenereDecrypt,
        "railfenceencrypt": RailfenceEncrypt,
        "railfencedecrypt": RailfenceDecrypt,
        "otpencrypt": OTPEncrypt,
        "otpdecrypt": OTPDecrypt,
    },
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

def GenerateCompleter(Map: dict[str, dict]) -> NestedCompleter:
    """Generate nested completer dict with parameter names for each function."""
    
    CompleterDict = {}
    
    for Module, Subcommand in Map.items():
        CompleterDict[Module] = {}
        for SubcommandName, CommandFunction in Subcommand.items():
            Signature = inspect.signature(CommandFunction)
            ParameterNames = list(Signature.parameters.keys())
            CompleterDict[Module][SubcommandName] = {Parameter: None for Parameter in ParameterNames}
    
    return NestedCompleter.from_nested_dict(CompleterDict)

MAINCOMPLETER    = GenerateCompleter(MAINCMDMAP)
PIDCOMPLETER     = GenerateCompleter(PIDCMDMAP)
HOHMANNCOMPLETER = GenerateCompleter(HOHMANNCMDMAP)

if __name__ == "__main__":
    _mainEnv()                       