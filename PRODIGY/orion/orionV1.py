"""ORION Engineering Assistant CLI - V.1"""

import os, json, math, numpy, shlex
from prompt_toolkit import prompt
from prompt_toolkit.completion import NestedCompleter
from typing_extensions import Callable
from typing import Literal

#UNIMAKE                                                                     .

#dB to linear scale and back                                                 .
#Significant figures rounding                                                .

# Will be implemented in V2:                                                 .

#UNICON                                                                      .

#PID output from error, integral, derivative terms                           .
#Natural frequency of a spring-mass system                                   .
#Damping ratio                                                               .

#UNIFLIGHT                                                                   .

#Lift equation from air density, velocity, area, lift coefficient            .
#Drag equation — same structure as lift                                      .
#Reynolds number from velocity, length, viscosity                            .
#Tsiolkovsky rocket equation — delta-v from exhaust velocity and mass ratio  .
#Dynamic pressure from air density and velocity                              .

#UNIMAKE                                                                     .

#Moment of inertia for common shapes (cylinder, rod, disk)                   .
#Mechanical advantage of a lever                                             .
#Stress and strain from force and cross-sectional area                       .

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

### ERRORS

class InvalidColorCount(Exception):
    """Raised when the color count passed into a function of the resistor group is invalid."""
    def __init__(self, Function: Callable):
        super().__init__(f"Invalid Color Count for {Function}")
class EmptyTokenList(Exception):
    """Raises when the TokenList passed into VerifyTokens() is empty."""
    def __init__(self):
        super().__init__(f"Empty TokenList! Make sure of correct tokens before verification attempt.")
class IncorrectArgumentCount(Exception):
    """Raises when the count of arguments given to a function is incorrect."""
    def __init__(self, function: Callable, GivenArgumentCount: int, WantedArgumentCount: set):
        super().__init__(f"Incorrect count of arguments for {function}. {function} takes {WantedArgumentCount} but was given {GivenArgumentCount}")
class UnknownModule(Exception):
    """Raises when an unknown module gets caught in VerifyTokens()."""
    def __init__(self, GivenModule: str):
        super().__init__(f"Unknown Module: {GivenModule}")
class UnknownSubCommand(Exception):
    """Raises when an unknown subcommand gets caught in VerifyTokens()."""
    def __init__(self, Module: str, GivenCommand: str):
        super().__init__(f"Unknown command for {Module}: {GivenCommand}")
class MissingSubCommand(Exception):
    """Raises when the subcommand is missing from a command string."""
    def __init__(self, module):
        super().__init__(f"Missing subcommand for {module}")    
class InvalidColors(Exception):
    """Raises when the colors passed into ResistorInsight() are invalid for the given band."""
    def __init__(self, function: Callable, IndexOfInvalidColors: list):
        super().__init__(f"Invalid colors for {function} at indices {IndexOfInvalidColors}")
class MissingParameters(Exception):
    """Raises when a function is not given enough parameters."""
    def __init__(self, Function: Callable, MissingParameters: list):
        super().__init__(f"Missing parameter {MissingParameters} for {Function}.")
class InconsistencyError(Exception):
    """Raises when the VIR-values passed into PowerDissipation() gives inconsistent values for the three formulas."""
    def __init__(self, Function: Callable, Inconsistency: str):
        super().__init__(Function, Inconsistency)

### UTILS

def InsertJSON(PathToJSON: str, ContentDict: dict) -> bool:
    try:
        with open(PathToJSON, 'w') as JSONFile:
            json.dump(ContentDict, JSONFile, indent=4, sort_keys=True)
            return True
    except Exception:
        return False
def ExtractJSON(PathToJSON: str) -> dict:
    with open(PathToJSON, 'r', encoding='utf-8') as file:
        ReturnDict = json.load(file)
        return ReturnDict
def ColorText(Text: str, Color: str):
        ansi = ANSI_COLORS.get(Color.lower(), "\033[0m")
        reset = "\033[0m"
        return ansi + Text + reset
    
### SYSTEM

def Tokenize(RawCommandString: str) -> list[str]:
    """Tokenize a raw command string and return token list."""
    return shlex.split(RawCommandString)
def dispatcher(RawCommandString: str):
    Tokens = Tokenize(RawCommandString) 
    VerifyTokens(Tokens)
    ValidateArgs(Tokens)
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
            
    return COMMANDMAP[Module][Command](*Args)

### UNIPOWER

def OhmsLaw(V: float | None = None, I: float | None = None, R: float | None = None) -> str:
    """Ohms Law calculation for Voltage, Current, and Resistivity.
    V = I * R
    I = V / R
    R = V / I
    """
    for value in (V, I, R):
        if value is not None:
            value = float(value)
            
    if (V, I, R).count(None) > 1:
        MissingParams = []
        for idx, value in enumerate((V, I, R)):
            if value is None:
                MissingParams.append(("V", "I", "R")[idx])
        
        raise MissingParameters(OhmsLaw, MissingParams)
    
    if V == None:
        V = I * R
    elif I == None:
        I = V / R
    elif R == None:
        R = V / I
        
    return f"V: {V}, I: {I}, R: {R}"
def VoltDivider(VIn: float, R1: float, R2: float) -> float:
    return VIn * (R2 / (R1 + R2))
def RCTimeConstant(Capacitance: float, Resistance: float) -> float:
    return Capacitance * Resistance
def InductorImpedance(Hertz: float, Inductance: float) -> float:
    return 2 * numpy.pi * Hertz * Inductance
def PowerDissipation(V: float | None = None, I: float | None = None, R: float | None = None) -> float:
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
        return P
    
    else:
        P1 = I ** 2 * R
        P2 = V ** 2 / R
        P3 = V * I
        
        if math.isclose(P1, P2):
            if math.isclose(P2, P3):
                return (P1 + P2 + P3) / 3
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

def TotalESR(caps: list[tuple], ConnectionType: Literal["parallel", "series"]) -> float:
    if ConnectionType == "series":
        return sum(cap[2] for cap in caps)
    elif ConnectionType == "parallel":
        try:
            return 1 / sum(1 / cap[2] for cap in caps if cap[2] != 0)
        except ZeroDivisionError:
            return 0  
    else:
        raise ValueError("Connection type must be 'parallel' or 'series'")
def TotalCapacitance(caps: list[tuple], ConnectionType: Literal["parallel", "series"]) -> tuple: ### caps (capacitance, voltage, esr) (for now)
    if ConnectionType == "parallel":
        TotalCapacitance = 0
        for cap in caps:
            TotalCapacitance += cap[0]
        VoltLimit = min([cap[1] for cap in caps])
    else: # series connection
        RawTotalCapacitance = 0
        for cap in caps:
            RawTotalCapacitance += ((cap[0])**(-1))
        TotalCapacitance = RawTotalCapacitance**(-1)
        VoltLimit = sum([cap[1] for cap in caps])     
    return (TotalCapacitance, VoltLimit, TotalESR(caps, ConnectionType))

### UNIMAKE

def Torque(MomentArmDistance: float, Force: float) -> float:
    """Returns torque in newtons from moment arm distance and force."""
    return MomentArmDistance * Force
def GearRatio(DrivingGearTeethCount: int, DrivenGearTeethCount: int) -> str:
    """Returns the gear ratio from the driving gear's teeth count and the driven gear's teeth count."""
    Ratio = DrivenGearTeethCount / DrivingGearTeethCount
    if Ratio > 1:
        return f"{Ratio} - {ColorText('Speed-', 'red')} - {ColorText('Torque+', 'green')}"
    elif Ratio < 1:
        return f"{Ratio} - {ColorText('Speed+', 'green')} - {ColorText('Torque-', 'red')}"
    else:
        return f"{Ratio} - Same Speed - Same Torque"
def AngularVelocityR(RPM: float) -> float:
    """Returns angular velocity from RPM in radians/s"""
    return RPM * numpy.pi / 30
def AngularVelocityD(RPM: float) -> float:
    """Returns angular velocity from RPM in degrees/s"""
    return R2D((RPM * numpy.pi / 30))
def KineticEnergy(Mass: float, Velocity: float) -> float:
    """Returns the kinetic energy from mass in KGs and velocity in meters/s"""
    return (0.5 * Mass * Velocity**2)
def PotentialEnergy(Mass: float, Height: float, Gravity: float | None = 9.8) -> float:
    """Returns the potential energy of a mass. Gravity is defaulted to 9.8m /s^2"""
    return Mass * Gravity * Height

def PSI2Pascal(PSI: float) -> float:
    return PSI * 6894,76
def Pascal2PSI(Pascal: float) -> float:
    return Pascal / 6894,76

### UNIFLIGHT

def T2WRatio(Thrust: float, Weight: float) -> float:
    """Thrust to Weight ratio calculator. Ensure consistent units!"""
    Ratio = Thrust / Weight
    return f"Ratio: {ColorText(f'{Ratio}', 'green' if Ratio > 1 else 'red')}" if Ratio != 1 else f"Ratio: {ColorText(f'{Ratio}', 'yellow')}"

def MachNumber(Velocity: float, SpeedOfSound: float | None = 343) -> float:
    """Mach Number Calulator. Use m/s!"""
    MachNumber = Velocity / SpeedOfSound
    return (f"Ratio: {ColorText(f'{MachNumber} - SUPERSONIC', 'green') if MachNumber > 1 else ColorText(f'{MachNumber} - SUBSONIC', 'red')}" if MachNumber != 1 else f"Ratio: {ColorText(f'{MachNumber} - TRANSONIC', 'yellow')}") if MachNumber < 5 else f"Ratio: {ColorText(f'{MachNumber} - HYPERSONIC', 'blue')}"

def Kilo2Newton(Kilo: float) -> float:
    return Kilo * 9.8
def Newton2Kilo(Newton: float) -> float:
    return Newton / 9.8

def MPS2KMH(MPS: float) -> float:
    return MPS * 3.6
def KMH2MPS(KMH: float) -> float:
    return KMH / 3.6

def DynamicPressure(Velocity: float, AirDensity: float | None = 1.225) -> float:
    return 0.5 * Velocity ** 2 * AirDensity

### UNIMATH

def TriExtrapolate(a: float, b: float, c: float, A: float | None = None, B: float | None = None, C: float | None = None) -> str:
    """Extrapolate the sides of a triangle from the AAAS case (3x Angle + 1x Side)"""

    SinA = math.sin(math.radians(a))
    SinB = math.sin(math.radians(b))
    SinC = math.sin(math.radians(c))
    
    if A is not None:
        B = (A * SinB) / SinA
        C = (A * SinC) / SinA
        
    elif B is not None:
        A = (B * SinA) / SinB
        C = (B * SinC) / SinB
        
    elif C is not None:
        A = (C * SinA) / SinC
        B = (C * SinB) / SinC
        
    Area = HeronsFormula(A, B, C)
    
    return f"""Area: {Area} - Sides: A: {A}, B: {B}, C: {C} - Sin({a}) = {SinA}, Sin({b}) = {SinB}, Sin({c}) = {SinC}"""

def Quadratic(A: float, B: float, C: float) -> tuple[float]:
    """Solves quadratic equations and returns x-values in a tuple."""
    if A == 0:
        return ValueError("Invalid quadratic equation! A cannot be 0.")
    D = B**2 - 4*A*C
    if D > 0:
        x1 = (-B - math.sqrt(D)) / (2 * A)
        x2 = (-B + math.sqrt(D)) / (2 * A)
        return (x1, x2)
    
    elif D == 0:
        x1 = -B / (2 * A)
        return (x1)
    
    else:
        return None

def D2R(Degrees: float) -> float:
    return Degrees / 180 * math.pi
def R2D(Radians: float) -> float:
    return Radians / math.pi * 180

def SineRule(
    Sides: list[float | None],
    Angles: list[float | None],
    AngleMeasurementMode: Literal["Degrees", "Radians"]
) -> list[list[float], list[float]] | None:
    """
    Sine Rule

    Formula: A / sin(a) = B / sin(b) = C / sin(c)

    Return Format: [Angles:[A, B, C], Sides:[A, B, C]]
    """
   
    angles_rad = []
    for angle in Angles:
        if angle is not None and AngleMeasurementMode == "Degrees":
            angles_rad.append(math.radians(angle))
        else:
            angles_rad.append(angle)

    known_angle_indices = [i for i in range(3) if angles_rad[i] is not None]
    if len(known_angle_indices) == 2:
        missing = next(i for i in range(3) if angles_rad[i] is None)
        angles_rad[missing] = math.pi - sum(angles_rad[i] for i in known_angle_indices)

    ReferenceRatio = None
    for idx in range(3):
        if Sides[idx] is not None and angles_rad[idx] is not None:
            ReferenceRatio = Sides[idx] / math.sin(angles_rad[idx])
            break

    ### Return None if no reference ratio could be established, meaning there is not enough information to solve the triangle.
    if ReferenceRatio is None:
        return None

    for idx in range(3):
        if Sides[idx] is None and angles_rad[idx] is not None:
            Sides[idx] = ReferenceRatio * math.sin(angles_rad[idx])
        elif angles_rad[idx] is None and Sides[idx] is not None:
            value = Sides[idx] / ReferenceRatio
            if not -1 <= value <= 1:
                return None
            asin_val = math.asin(value)
            known_sum = sum(a for a in angles_rad if a is not None)
            
            ### Check for the ambiguous case of the sine rule, where there may be two possible angles that satisfy the equation
            if math.pi - asin_val + known_sum <= math.pi:
                angles_rad[idx] = math.pi - asin_val
            else:
                angles_rad[idx] = asin_val

    if AngleMeasurementMode == "Degrees":
        Angles_out = [math.degrees(a) if a is not None else None for a in angles_rad]
    else:
        Angles_out = angles_rad

    return [Angles_out, Sides]

def CosineRule(LengthA: float, LengthB: float, AngleA: float) -> float:
    return math.sqrt(LengthA ** 2 + LengthB ** 2 - ((2 * LengthA * LengthB) * math.cos(math.radians(AngleA))))
def ReverseCosineRule(LengthA: float, LengthB: float, LengthC: float) -> tuple[float]:
    """ 
    Returns a tuple of the three angles in degrees, in the order of AngleA, AngleB, AngleC 
    
    Formula: AngleA = arccos((B^2 + C^2 - A^2) / (2BC))
    """

    return (
        math.degrees(math.acos((LengthB ** 2 + LengthC ** 2 - LengthA ** 2) / (2 * LengthB * LengthC))),  # AngleA
        math.degrees(math.acos((LengthC ** 2 + LengthA ** 2 - LengthB ** 2) / (2 * LengthC * LengthA))),  # AngleB
        math.degrees(math.acos((LengthA ** 2 + LengthB ** 2 - LengthC ** 2) / (2 * LengthA * LengthB)))   # AngleC
    )

def SASArea(LengthA: float, LengthB: float, AngleC: float) -> float:
    return (0.5 * LengthA * LengthB * math.sin(math.radians(AngleC)))
def HeronsFormula(LengthA: float, LengthB: float, LengthC: float) -> float:
    """
    Returns the area of a triangle from the side lengths.

    Args:
        LenghtA (float):
        LenghtB (float):
        LenghtC (float):

    Returns:
        Area (float):
    """
    S = (LengthA + LengthB + LengthC) / 2
    return math.sqrt(S * (S - LengthA) * (S - LengthB) * (S - LengthC))

### UNIALGO

def FibonacciList(ListLength: float) -> list[int]:
    """Fibonacci sequence generator"""
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
    """Fibonacci integer generator"""   
    try:
        FiboIndex = int(FiboIndex)  
    except ValueError:
        raise ValueError("FibonacciInteger does not take floats or strings!")       
    fib0, fib1 = 0, 1
    for _ in range(0, (FiboIndex - 2)):
        fib2 = fib0 + fib1
        fib0, fib1 = fib1, fib2
        
    return fib2

def LovelacesAlgorithm(a: float, b: float, c: float, d: float, e: float, f: float) -> tuple:
    """Lovelace's algorithm for solving systems of linear equations"""
    D = a*e - b*d
    if D == 0:
        raise ValueError("The system has no unique solution.")
    
    Dx = c*e - b*f
    Dy = a*f - c*d
    x = Dx / D
    y = Dy / D
    return (x, y)

### UNICRYPT

def BinaryEncrypt(InputString: str) -> str:
    RawBinary = ''.join(format(ord(i), '08b') for i in InputString)
    OutputString = ' '.join(RawBinary[i:i+8] for i in range(0, len(RawBinary), 8))
    return OutputString
def BinaryDecrypt(InputString: str) -> str:
    OutputString = ''.join(chr(int(b, 2)) for b in InputString.split())
    return OutputString
def CeasarEncrypt(InputString: str, Shift: int) -> str:
    OutputString = ""
    for Character in InputString:
        if Character.isalpha():               
            Position = ord(Character.lower()) - 96 
            NewPosition = (Position + Shift - 1) % 26 + 1   
            NewCharacter = chr(NewPosition + 96)        
            OutputString += NewCharacter                
        else:                                
            OutputString += Character 
    return OutputString
def CeasarDecrypt(InputString: str, Shift: int) -> str:
    OutputString = ""
    for Character in InputString:
        if Character.isalpha():               
            Position = ord(Character.lower()) - 96
            NewPosition = (Position - Shift - 1) % 26 + 1   
            NewCharacter = chr(NewPosition + 96)        
            OutputString += NewCharacter                
        else:                                 
            OutputString += Character
    return OutputString 
def VigenereEncrypt(InputString: str, KeyString: str) -> str:
    OutputString = ""

    for idx, Character in enumerate(InputString):
        if Character.isalpha():
            if Character.isupper():
                OutputString += chr((ord(Character) - ord(KeyString[idx % len(KeyString)].upper()) + 26) % 26 + ord("A"))
            else:
                OutputString += chr((ord(Character) - ord(KeyString[idx % len(KeyString)].lower()) + 26) % 26 + ord("a"))
        else:
            OutputString += Character
    return OutputString
def VigenereDecrypt(InputString: str, KeyString: str) -> str:
    OutputString = ""
    KeyString = KeyString.lower()
    KeyIdx = 0

    for Character in InputString:
        if Character.isalpha():
            Shift = ord(KeyString[KeyIdx % len(KeyString)]) - ord('a')
            if Character.isupper():
                DecryptedCharacter = chr((ord(Character) - ord('A') - Shift + 26) % 26 + ord('A'))
            else:
                DecryptedCharacter = chr((ord(Character) - ord('a') - Shift + 26) % 26 + ord('a'))
            OutputString += DecryptedCharacter
            KeyIdx += 1
        else:
            OutputString += Character

    return OutputString
def RailfenceEncrypt(InputString: str, Key: int) -> str:
    Position = 0
    Direction = 1
    Rows = [[] for _ in range(Key)]

    for Character in InputString:
        Rows[Position].append(Character)
    
        Position += Direction
        if Position == 0 or Position == Key - 1:
            Direction *= -1
    
    return ''.join([''.join(Row) for Row in Rows])
def RailfenceDecrypt(InputString: str, Key: str) -> str:
    length = len(InputString)
    pattern = []
    pos = 0
    direction = 1
    for _ in range(length):
        pattern.append(pos)
        pos += direction
        if pos == 0 or pos == Key - 1:
            direction *= -1

    counts = [pattern.count(r) for r in range(Key)]
    rows = []
    index = 0
    for c in counts:
        rows.append(list(InputString[index:index + c]))
        index += c

    plaintext = ''
    row_pointers = [0] * Key
    for r in pattern:
        plaintext += rows[r][row_pointers[r]]
        row_pointers[r] += 1

    return plaintext
def OTPEncrypt(InputString: str, KeyString: str) -> str:
    bitext = ''.join(format(ord(i), '08b') for i in InputString)
    bikey = ''.join(format(ord(i), '08b') for i in KeyString)
    cipher = ''.join(str(int(b1) ^ int(b2)) for b1, b2 in zip(bitext, bikey))
    return ' '.join(cipher[i:i+8] for i in range(0, len(cipher), 8))
def OTPDecrypt(InputString: str, KeyString: str) -> str:
    bikey = ''.join(format(ord(i), '08b') for i in KeyString)
    plaintext_bits = ''.join(str(int(b1) ^ int(b2)) for b1, b2 in zip(InputString, bikey))
    return ''.join(chr(int(plaintext_bits[i:i+8], 2)) for i in range(0, len(plaintext_bits), 8))
    
### MAPS

ARGUMENTMAP: dict[str, set] = {
    "unipower": {
        "ohmslaw": {3},
        "voltdivider": {3},
        "rctimeconstant": {2},
        "inductorimpedance": {2},
        "powerdissipation": {3},
        "resistorinsight": {4, 5},
        "resistorviz": {4, 5},
        "capacitance": {2},
        "esr": {2},
    },
    "unimake": {
        "torque": {2},
        "gearratio": {2},
        "angularvelocityr": {1},
        "angularvelocityd": {1},
        "kineticenergy": {2},
        "potentialenergy": {3},
    },
    "uniflight": {
        "T2Wratio": {2},
        "machnumber": {2},
        "kilo2newton": {1},
        "newton2kilo": {1},
        "mps2kmh": {1},
        "kmh2mps": {1},
        "dynamicpressure": {1, 2},
    },
    "unimath": {
        "triextrapolate": {4, 6},
        "quadratic": {3},
        "D2R": {1},
        "R2D": {1},
        "sinerule": {7},
        "cosinerule": {3},
        "reversecosinerule": {3},
        "sasarea": {3},
        "herons": {3}
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
    }
}
COMMANDMAP: dict[str, dict[str, callable]] = {
    "unipower": {
        "ohmslaw": OhmsLaw,
        "voltdivider": VoltDivider,
        "rctimeconstant": RCTimeConstant,
        "inductorimpedance": InductorImpedance,
        "powerdissipation": PowerDissipation,
        "resistorinsight": ResistorInsight,
        "resistorviz": ResistorViz,
        "capacitance": TotalCapacitance,
        "esr": TotalESR,
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
        "kilo2newton": Kilo2Newton,
        "newton2kilo": Newton2Kilo,
        "mps2kmh": MPS2KMH,
        "kmh2mps": KMH2MPS,
        "dynamicpressure": DynamicPressure,
    },
    "unimath": {
        "triextrapolate": TriExtrapolate,
        "quadratic": Quadratic,
        "D2R": D2R,
        "R2D": R2D,
        "sinerule": SineRule,
        "cosinerule": CosineRule,
        "reversecosinerule": ReverseCosineRule,
        "sasarea": SASArea,
        "herons": HeronsFormula,
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
    }
}
COMPLETER = NestedCompleter.from_nested_dict({
    "unipower": {
        "ohmslaw": None,
        "voltdivider": None,
        "rctimeconstant": None,
        "inductorimpedance": None,
        "powerdissipation": None,
        "resistorinsight": None,
        "resistorviz": None,
        "capacitance": None,
        "esr": None,
    },
    "unimake": {
        "torque": None,
        "gearratio": None,
        "angularvelocityr": None,
        "angularvelocityd": None,
        "kineticenergy": None,
        "potentialenergy": None,
    },
    "uniflight": {
        "T2Wratio": None,
        "machnumber": None,
        "kilo2newton": None,
        "newton2kilo": None,
        "mps2kmh": None,
        "kmh2mps": None,
        "dynamicpressure": None,
    },
    "unimath": {
        "triextrapolate": None,
        "quadratic": None,
        "D2R": None,
        "R2D": None,
        "sinerule": None,
        "cosinerule": None,
        "reversecosinerule": None,
        "sasarea": None,
        "herons": None,
    },
    "unialgo": {
        "fibonaccilist": None,
        "fibonacciinteger": None,
        "lovelacesalgorithm": None,
    },
    "unicrypt": {
        "binaryencrypt": None,
        "binarydecrypt": None,
        "ceasarencrypt": None,
        "ceasardecrypt": None,
        "vigenereencrypt": None,
        "vigeneredecrypt": None,
        "railfenceencrypt": None,
        "railfencedecrypt": None,
        "otpencrypt": None,
        "otpdecrypt": None,
    }
})

### SYSTEM

def VerifyTokens(TokenList: list) -> bool:
    """Verify validity of tokens before dispatching."""
    if not TokenList: 
        raise EmptyTokenList
    elif TokenList[0] not in COMMANDMAP:
        raise UnknownModule(TokenList[0])
    elif len(TokenList) < 2:
        raise MissingSubCommand(TokenList[0])
    elif TokenList[1] not in COMMANDMAP[TokenList[0]]:
        raise UnknownSubCommand(TokenList[0], TokenList[1])
    else:
        return True
def ValidateArgs(TokenList: list) -> bool:
    """Validate that the arguments passed into a function are of the correct length."""
    Module, Command, Args = TokenList[0], TokenList[1], TokenList[2:]
    if len(Args) not in ARGUMENTMAP[Module][Command]:
        raise IncorrectArgumentCount(COMMANDMAP[Module][Command], len(Args), ARGUMENTMAP[Module][Command])
    else:
        return True

### RECIEVE EVAL PRINT LOOP

def REPL() -> None:
    os.system('cls')
    while True:        
        try:
            CommandString = prompt("ORION >>> ", completer=COMPLETER)
            print(dispatcher(CommandString))
            
        except Exception as e:
            print(e)   

if __name__ == "__main__":
    REPL()
                               