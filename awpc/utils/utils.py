"""The `AWPC` utilities and dependencies module. This module contains all the dependencies of the `AWPC` library, such as custom exceptions, datatypes, and other utilities."""

import inspect
from prompt_toolkit.completion import NestedCompleter

### ERRORS

class ImpossibleTriangleError(Exception):
    """Raise when the sum of the angles of a triangle is not 180 degrees, a mathematical impossibility."""
    def __init__(self):
        super().__init__("The sum of the angles of a triangle can't be anything else than 180 degrees!")
class DimensionMismatch(Exception):
    """Raise when the dimensions of two units don't match when trying to convert or perform operations on them."""
    def __init__(self, string):
        super().__init__(string)
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
    
### MAPS
    
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

class Unit:
    """Base class for the unit system - unifying units of measurement along with the dimension of measurement (e.g. length, weight, etc.)"""
    def __init__(self, unit: float, measurement: str):
        self.unit = unit
        self.measurement = measurement
        
    def __str__(self):
        return self.unit
    def __repr__(self) -> str:
        return f"Unit({self.unit!r}, {self.measurement!r})"
    def __eq__(self, other):
        return isinstance(other, Unit) and self.unit == other.unit and self.measurement == other.measurement
    def __hash__(self):
        return hash((self.unit, self.measurement))
 
class Quantity:
    """Base Class for storing values and their units."""
    def __init__(self, value: float, unit: Unit):
        self._value = value
        self.unit = unit
        
    @property
    def value(self):
        return self._value
        
    def __str__(self):
        return f"{self._value} {self.unit}"
    def __repr__(self):
        return f"Quantity({self.value!r}, {self.unit!r})"
    def __mul__(self, other):
        if isinstance(other, Quantity):
            return self._value * other._value
        return self._value * other
    def __rmul__(self, other):
        return self.__mul__(other) 
    def __truediv__(self, other):
        if isinstance(other, Quantity):
            return self._value / other._value
        return self._value / other
    def __rtruediv__(self, other):
        return other / self._value
class PhysicalConstant:
    """Physical Constant class for fixed constants that can't be changed nor converted."""
    def __init__(self, value: float, unit: Unit, name: str):
        self._value = value
        self.unit = unit 
        self.name = name
        
    @property
    def value(self):
        return self._value
    
    def __str__(self):
        return f"{self.name}: {self._value} {self.unit}"
    def __repr__(self):
        return f"PhysicalConstant({self._value!r}, {self.unit!r}, {self.name!r})"    
    def __mul__(self, other):
        if isinstance(other, PhysicalConstant):
            return self._value * other._value
        return self._value * other
    def __rmul__(self, other):
        return self.__mul__(other) 
    def __truediv__(self, other):
        if isinstance(other, PhysicalConstant):
            return self._value / other._value
        return self._value / other
    def __rtruediv__(self, other):
        return other / self._value
          
UNITS: dict[str, Unit] = {
    "m":    Unit("m",    "length"),
    "km":   Unit("km",   "length"),
    "ft":   Unit("ft",   "length"),
    
    "m/s":  Unit("m/s",  "velocity"),
    "km/h": Unit("km/h", "velocity"),
    "knot": Unit("knot", "velocity"),
    
    "kg":   Unit("kg",   "Weight"),
    "kt":   Unit("kt",   "Weight"),
    "mt":   Unit("mt",   "Weight"),
    
    "N":    Unit("N",    "force"),
    "kgf":  Unit("kgf",  "force"),
    
    "pa":   Unit("Pa",   "pressure"),
    "psi":  Unit("psi",  "pressure"),
    
    "Deg":  Unit("Deg",  "Angles"),
    "Rad":  Unit("Rad",  "Angles"),
    
    "J":    Unit("J",    "Energy"),
    "W":    Unit("W",    "Energy"),
    
    "S":    Unit("S",    "time"),
    "M":    Unit("M",    "time"),
    
    "Nm":   Unit("Nm", "Torque"),
        
    "A":    Unit("A",    "Current"),
    
    "V":    Unit("V",    "Voltage"),
    
    "Δv":   Unit("Δv",   "Change in Velocity"),
    
    "Ohm":  Unit("Ω",    "ERI"),    # Electrical resistance / impedance
    
    "m/s^2": Unit("m/s^2", "acceleration"),
    
    "GCONST": Unit("Nm^2/kg^2", "gravity"),
}
CONVERSION_TABLE: dict[tuple[str, str], float] = {
    # Velocity
    ("m/s",  "km/h"): 3.6,
    ("km/h", "m/s"):  1 / 3.6,
    # Force
    ("N",    "kgf"):  1 / 9.81,
    ("kgf",  "N"):    9.81,
    # Pressure
    ("Pa",   "psi"):  1 / 6894.76,
    ("psi",  "Pa"):   6894.76,
}

def Convert(GivenQuantity: Quantity, TargetUnit: Unit) -> Quantity:
    """Convert one quantity to a new unit of the same dimension."""
    
    if GivenQuantity.unit == TargetUnit:
        return GivenQuantity
    
    if GivenQuantity.unit.measurement == TargetUnit.measurement:
        raise DimensionMismatch(f"Units {GivenQuantity.unit.measurement} and {TargetUnit.measurement} are not of the same dimension! Cannot convert.")
    
    key = (GivenQuantity.unit.unit, TargetUnit.unit)
    if key not in CONVERSION_TABLE:
        raise KeyError(f"No conversion defined from {GivenQuantity.unit} to {TargetUnit}")
    
    return Quantity(GivenQuantity.value * CONVERSION_TABLE[key], TargetUnit)
def ColorText(Text: str, Color: str) -> str:
    """Returns the given text in the given color using `ANSI` escape codes. If the color is not found, it returns the text without coloring."""
    Text = str(Text)
    ANSI = ANSI_COLORS.get(Color.lower(), '\033[0m')
    return ANSI + Text + '\033[0m'
def GenerateCompleter(Map: dict[str, dict]) -> NestedCompleter:
    """Generate a `NestedCompleter` dict with parameter names for each function."""
    
    CompleterDict = {}
    
    for Module, Subcommand in Map.items():
        CompleterDict[Module] = {}
        for SubcommandName, CommandFunction in Subcommand.items():
            Signature = inspect.signature(CommandFunction)
            CompleterDict[Module][SubcommandName] = {param: None for param in Signature.parameters}
    
    return NestedCompleter.from_nested_dict(CompleterDict)

G = PhysicalConstant(6.6743 * 1e-11, UNITS["GCONST"], "Gravitational Constant")
C = PhysicalConstant(299792458, UNITS["m/s"], "Speed of Light")
AU = PhysicalConstant(1.496e+11, UNITS["m"], "Astronomical Unit")
MACH = PhysicalConstant(343, UNITS["m/s"], "Speed of Sound at sea level")

EARTH_G = PhysicalConstant(9.8,  UNITS["m/s^2"], "Surface Gravity of the Earth")
MOON_G  = PhysicalConstant(1.62, UNITS["m/s^2"], "Surface Gravity of the Moon")
MARS_G  = PhysicalConstant(3.71, UNITS["m/s^2"], "Surface Gravity of Mars")
SUN_G   = PhysicalConstant(274,  UNITS["m/s^2"], "Surface Gravity of the Sun")

EARTH_M = PhysicalConstant(5.972e+24, UNITS["kg"], "Mass of the Earth")
MOON_M  = PhysicalConstant(7.342e+22, UNITS["kg"], "Mass of the Moon")
MARS_M  = PhysicalConstant(6.390e+23, UNITS["kg"], "Mass of Mars")
SUN_M   = PhysicalConstant(1.989e+30, UNITS["kg"], "Mass of the Sun")

EARTH_R = PhysicalConstant(6.371e+6, UNITS["m"], "Radius of the Earth")
MOON_R  = PhysicalConstant(1.737e+6, UNITS["m"], "Radius of the Moon")
MARS_R  = PhysicalConstant(3.390e+6, UNITS["m"], "Radius of Mars")
SUN_R   = PhysicalConstant(6.957e+8, UNITS["m"], "Radius of the Sun")
