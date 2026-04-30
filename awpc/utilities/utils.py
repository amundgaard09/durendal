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

def xColorText(Text: str, Color: str) -> str:
    """Returns the given text in the given color using `ANSI` escape codes. If the color is not found, it returns the text without coloring."""
    Text = str(Text)
    ANSI = ANSI_COLORS.get(Color.lower(), '\033[0m')
    return ANSI + Text + '\033[0m'
def InsertJSON(PathToJSON: str, ContentDict: dict) -> None:
    """Inserts a dictionary into a `JSON` file. If the file does not exist, it creates it. Returns `True` if the operation was successful, `False` otherwise."""
    
    import json
    
    with open(PathToJSON, 'w') as JSONFile:
        json.dump(ContentDict, JSONFile, indent=4, sort_keys=True)
def ExtractJSON(PathToJSON: str) -> dict:
    """Extracts a `JSON` file and returns the content as a dictionary. Returns `None` if the file is not found or if there is an error during extraction."""
    
    import json
    
    try:
        with open(PathToJSON, 'r', encoding='utf-8') as file:
            return json.load(file)
    except Exception:
        return None

G       = PhysicalConstant(6.674e-11, UNITS["GCONST"], "Gravitational Constant")
C       = PhysicalConstant(299792458, UNITS["m/s"],    "Speed of Light")
AU      = PhysicalConstant(1.496e+11, UNITS["m"],      "Astronomical Unit")
MACH    = PhysicalConstant(343,       UNITS["m/s"],    "Speed of Sound at sea level")

EARTH_G = PhysicalConstant(9.8,       UNITS["m/s^2"],  "Surface Gravity of the Earth")
MOON_G  = PhysicalConstant(1.62,      UNITS["m/s^2"],  "Surface Gravity of the Moon")
MARS_G  = PhysicalConstant(3.71,      UNITS["m/s^2"],  "Surface Gravity of Mars")
SUN_G   = PhysicalConstant(274,       UNITS["m/s^2"],  "Surface Gravity of the Sun")

EARTH_M = PhysicalConstant(5.972e+24, UNITS["kg"],     "Mass of the Earth")
MOON_M  = PhysicalConstant(7.342e+22, UNITS["kg"],     "Mass of the Moon")
MARS_M  = PhysicalConstant(6.390e+23, UNITS["kg"],     "Mass of Mars")
SUN_M   = PhysicalConstant(1.989e+30, UNITS["kg"],     "Mass of the Sun")

EARTH_R = PhysicalConstant(6.371e+6,  UNITS["m"],      "Radius of the Earth")
MOON_R  = PhysicalConstant(1.737e+6,  UNITS["m"],      "Radius of the Moon")
MARS_R  = PhysicalConstant(3.390e+6,  UNITS["m"],      "Radius of Mars")
SUN_R   = PhysicalConstant(6.957e+8,  UNITS["m"],      "Radius of the Sun")
