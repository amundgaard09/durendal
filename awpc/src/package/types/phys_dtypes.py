"""
This module contains the base classes for the custom data types used in the `AWPC` library, such as the unit system, including `Unit`, `Quantity`, and `PhysicalConstant`.
"""

# Alpha - A α, Beta - B β, Gamma - Γ γ, Delta - Δ δ,  Epsilon - E ε, Zeta - Z ζ, Eta - H η, 
# Theta - Θ θ, Iota - I ι, Kappa - K κ, Lambda - Λ λ, Mu - M μ,      Nu - N ν,   Xi - Ξ ξ,  Omicron - O ο, 
# Pi - Π π,    Rho - P ρ,  Sigma - Σ σ ς, Tau - T τ,  Ypsilon - Y υ, Phi - Φ φ,  Chi - X χ, Psi - Ψ ψ, Omega - Ω ω

class Unit:
    """Base class for the unit system - unifying units of measurement along with the dimension of measurement (e.g. length, weight, etc.)"""
    def __init__(self, unitname: str, measurement: str):
        self.unitname = unitname
        self.measurement = measurement
        
    def __str__(self):
        return self.unitname
    def __repr__(self) -> str:
        return f"Unit({self.unitname!r}, {self.measurement!r})"
    def __eq__(self, other):
        return isinstance(other, Unit) and self.unitname == other.unitname and self.measurement == other.measurement
    def __hash__(self):
        return hash((self.unitname, self.measurement))
    def __bool__(self):
        return True   
class Quantity:
    """Base Class for storing values and their units."""
    def __init__(self, value: float, unit: Unit):
        self._value = value
        self._unit = unit
        
    def __str__(self) -> str:
        return f"{self._value} - {self._unit}"    
    def __repr__(self) -> str:
        return f"Quantity({self._value!r}, {self._unit!r})"
    def __eq__(self, other) -> bool:
        return isinstance(other, Quantity) and self._unit == other._unit and self._value == other._value
    def __hash__(self) -> int:
        return hash((self._value, self._unit))
    def __bool__(self) -> bool:
        return self._value != 0
    def __neg__(self) -> float:
        return -self._value
    def __abs__(self) -> float:
        return abs(self._value)
    
    def __add__(self, other):
        if isinstance(other, self.__class__):
            return self._value + other._value
        return self._value + other 
    def __radd__(self, other):
        if isinstance(other, self.__class__):
            return other._value + self._value
        return other + self._value 
    def __sub__(self, other):
        if isinstance(other, self.__class__):
            return self._value - other._value
        return self._value - other 
    def __rsub__(self, other):
        if isinstance(other, self.__class__):
            return other._value - self._value
        return other - self._value 
    def __mul__(self, other):
        if isinstance(other, self.__class__):
            return self._value * other._value
        return self._value * other
    def __rmul__(self, other):
        if isinstance(other, self.__class__):
            return other._value * self._value
        return other * self._value 
    def __truediv__(self, other):
        if isinstance(other, self.__class__):
            return self._value / other._value
        return self._value / other
    def __rtruediv__(self, other):
        if isinstance(other, self.__class__):
            return other._value / self._value
        return other / self._value
    def __floordiv__(self, other):
        if isinstance(other, self.__class__):
            return self._value // other._value
        return self._value // other
    def __rfloordiv__(self, other):
        if isinstance(other, self.__class__):
            return other._value // self._value
        return other // self._value
    def __mod__(self, other):
        if isinstance(other, self.__class__):
            return self._value % other._value
        return self._value % other
    def __rmod__(self, other):
        if isinstance(other, self.__class__):
            return other._value % self._value
        return other % self._value
    def __pow__(self, other):
        if isinstance(other, self.__class__):
            return self._value ** other._value
        return self._value ** other
    def __rpow__(self, other):
        if isinstance(other, self.__class__):
            return other._value ** self._value
        return other ** self._value
class PhysicalConstant(Quantity):
    """Physical Constant class for fixed constants that can't be changed nor converted."""
    def __init__(self, value: float, unit: Unit, name: str):
        super().__init__(value, unit)
        self._name = name
    
    def __str__(self):
        return f"{self._name}: {self._value} - {self._unit}"
    def __repr__(self) -> str:
        return f"PhysicalConstant({self._value!r}, {self._unit!r}, {self._name!r})"
    
UNITS: dict[str, Unit] = {
    "am": Unit("Attometer",  "Length"), 
    "fm": Unit("Femtometer", "Length"),
    "pm": Unit("Picometer",  "Length"),
    "nm": Unit("Nanometer",  "Length"),
    "μm": Unit("Micrometer", "Length"),
    "mm": Unit("Millimeter", "Length"),
    "cm": Unit("Centimeter", "Length"),
    "in": Unit("Inch",       "Length"),
    "dm": Unit("Decameter",  "Length"),
    "ft": Unit("Foot",       "Length"),
    "Yd": Unit("Yard",       "Length"),
     "m": Unit("Meter",      "Length"),
    "km": Unit("Kilometer",  "Length"),
    "mi": Unit("Mile",       "Length"),
    "ly": Unit("Light year", "Length"),
  "psrc": Unit("Parsec",     "Length"),
    
    "m²": Unit("Square Meter",     "Area"), 
   "km²": Unit("Square Kilometer", "Area"), 
   "ft²": Unit("Square Foot",      "Area"), 
   "acr": Unit("Acre",             "Area"),
    
    "mL": Unit("Milliliter",  "Volume"),
     "L": Unit("Liter",       "Volume"), 
   "gal": Unit("Gallon",      "Volume"), 
   "ft³": Unit("Cubic Foot",  "Volume"),
    "m³": Unit("Cubic Meter", "Volume"), 
    
    "ag": Unit("Attogram",  "Mass"),
    "fg": Unit("Femtogram", "Mass"),
    "pg": Unit("Picogram",  "Mass"),
    "ng": Unit("Nanogram",  "Mass"),
    "μg": Unit("Microgram", "Mass"),
    "mg": Unit("Milligram", "Mass"),
     "g": Unit("Gram",      "Mass"),
    "oz": Unit("Ounce",     "Mass"),
    "lb": Unit("Pound",     "Mass"),
    "kg": Unit("Kilogram",  "Mass"),
     "t": Unit("Ton",       "Mass"),
    "kt": Unit("Kiloton",   "Mass"),
    "mt": Unit("Megaton",   "Mass"),
    "gt": Unit("Gigaton",   "Mass"),
    
    "ns": Unit("Nanosecond",  "Time"),
    "μs": Unit("Microsecond", "Time"),
    "ms": Unit("Millisecond", "Time"),
     "s": Unit("Second",      "Time"),
    "mi": Unit("Minute",      "Time"),
     "h": Unit("Hour",        "Time"),
   "day": Unit("Day",         "Time"),
    "wk": Unit("Week",        "Time"),
    "yr": Unit("Year",        "Time"),
    
     "J": Unit("Joule",        "Energy"),
   "cal": Unit("Calorie",      "Energy"),
   "kcl": Unit("Kilocalorie",  "Energy"),
   "kWh": Unit("Kilowatthour", "Energy"), 
    "eV": Unit("Electronvolt", "Energy"),
    
    "hp": Unit("Horsepower", "Power"),
     "W": Unit("Watt",       "Power"),
        
     "N": Unit("Newton",   "Force"),
   "kgf": Unit("Kg-force", "Force"),
   "lbf": Unit("lb-force", "Force"),
    
   "deg": Unit("Degree",  "Angles"),
   "rad": Unit("Radian",  "Angles"),
    
    "Δv":  Unit("Delta-V",    "Change in Velocity"),
    "°K":  Unit("Kelvin",     "Temperature"), 
    "°C":  Unit("Celsius",    "Temperature"), 
    "°F":  Unit("Fahrenheit", "Temperature"),
    
     "A": Unit("Ampere",  "Current"),
     "V": Unit("Volt",    "Voltage"),
     "Ω": Unit("Ohm",     "Resistance"),
     "C": Unit("Coloumb", "Electric Charge"),
     "F": Unit("Farad",   "Electric Capacitance"),
     "H": Unit("Henry",   "Magnetic Capacitance"),
     "T": Unit("Tesla",   "Magnetic Flux Density"),
     "G": Unit("Gauss",   "Magnetic Flux Density"),
    
    "Hz": Unit("Hertz",     "Frequency"),
   "kHz": Unit("Kilohertz", "Frequency"),
   "MHz": Unit("Megahertz", "Frequency"),
   "GHz": Unit("Gigahertz", "Frequency"),
    
    "pa": Unit("Pascal",     "Pressure"),
   "psi": Unit("Psi",        "Pressure"),
   "bar": Unit("Bar",        "Pressure"),
   "atm": Unit("Atmosphere", "Pressure"), 
  "torr": Unit("Torr",       "Pressure"),
  "mmHg": Unit("mm Mercury", "Pressure"),
    
   "m/s": Unit("Meter/Second",   "Velocity"),
   "mph": Unit("Miles/Hour",     "Velocity"),
  "km/h": Unit("Kilometer/Hour", "Velocity"),
  "knot": Unit("Knot",           "Velocity"),
    
  "m/s²": Unit("m/s²",  "Acceleration"),
 "ft/s²": Unit("ft/s²", "Acceleration"),
    
    "Nm": Unit("Newtonmeter", "Torque"),
 "ft-lb": Unit("Foot-pound",  "Torque"),
    
"GCONST": Unit("Nm²/kg²", "The Gravitational Constant"),
"NCONST": Unit("N/A",     "Unit for Numerical / Unitless Constants")
}

