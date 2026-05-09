"""
This module contains the base classes for the custom data types used in the `AWPC` library, such as the unit system, including `Unit`, `Quantity`, and `PhysicalConstant`.
"""

### UNIT SYSTEM

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

class _NumericValue:
    def __init__(self, value: float, unit: str):
        self._value = value
        self._unit  = unit
    
    @property
    def value(self):
        return self._value
    
    @property
    def unit(self):
        return self._unit
        
    def __int__(self):
        return int(self._value)
    def __float__(self):
        return self.value
    def __str__(self):
        return f"{self._value}"
    def __bool__(self):
        return True if self._value != 0 else False
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
class Quantity(_NumericValue):
    """Base Class for storing values and their units."""
    def __init__(self, value: float, unit: Unit):
        super().__init__(value, unit)
        
    def __str__(self):
        return f"{self.value} - {self.unit}"    
    def __repr__(self) -> str:
        return f"Quantity({self.value!r}, {self.unit!r})"
class PhysicalConstant(_NumericValue):
    """Physical Constant class for fixed constants that can't be changed nor converted."""
    def __init__(self, value: float, unit: Unit, name: str):
        super().__init__(value, unit) 
        self._name = name

    @property
    def name(self):
        return self._name
    
    def __str__(self):
        return f"{self.name}: {self.value} - {self.unit}"
    def __repr__(self) -> str:
        return f"PhysicalConstant({self.value!r}, {self.unit!r}, {self.name!r})"
    
UNITS: dict[str, Unit] = {
    "am": Unit("Attometer",  "Length"),
    "fm": Unit("Femtometer", "Length"),
    "pm": Unit("Picometer",  "Length"),
    "nm": Unit("Nanometer",  "Length"),
    "μm": Unit("Micrometer", "Length"),
    "mm": Unit("Millimeter", "Length"),
    "cm": Unit("Centimeter", "Length"),
    "ft": Unit("Foot",       "Length"),
    "m":  Unit("Meter",      "Length"),
    "km": Unit("Kilometer",  "Length"),
    "mi": Unit("Mile",       "Length"),
    "ly": Unit("Light year", "Length"),
    
    "m/s":  Unit("Meter/Second",   "Velocity"),
    "km/h": Unit("Kilometer/Hour", "Velocity"),
    "mph":  Unit("Miles/Hour",     "Velocity"),
    "knot": Unit("Knot",           "Velocity"),
    
    "ag": Unit("Attogram",  "Mass"),
    "fg": Unit("Femtogram", "Mass"),
    "pg": Unit("Picogram",  "Mass"),
    "ng": Unit("Nanogram",  "Mass"),
    "μg": Unit("Microgram", "Mass"),
    "mg": Unit("Milligram", "Mass"),
    "g":  Unit("Gram",      "Mass"),
    "kg": Unit("Kilogram",  "Mass"),
    "t":  Unit("Ton",       "Mass"),
    "kt": Unit("Kiloton",   "Mass"),
    "mt": Unit("Megaton",   "Mass"),
    "gt": Unit("Gigaton",   "Mass"),
    
    "N":   Unit("Newton",        "Force"),
    "kgf": Unit("Kilogramforce", "Force"),
    
    "pa":  Unit("Pascal", "Pressure"),
    "psi": Unit("Psi",    "Pressure"),
    
    "deg": Unit("Degree", "Angles"),
    "rad": Unit("Radian", "Angles"),
    
    "J": Unit("Joule", "Energy"),
    
    "W": Unit("Watt",  "Power"),
    
    "S": Unit("Second", "Time"),
    "M": Unit("Minute", "Time"),
    "H": Unit("Hour",   "Time"),
    "Y": Unit("Year",   "Time"),
    
    "Nm": Unit("Newtonmeter", "Torque"),
        
    "A": Unit("Ampere", "Current"),
    
    "V": Unit("Volt", "Voltage"),
    
    "Δv": Unit("Delta-V", "Change in Velocity"),
    
    "Ω": Unit("Ohm", "Resistance"),
    
    "m/s^2": Unit("m/s^2", "Acceleration"),
    
    "GCONST": Unit("Nm^2/kg^2", "Gravity"),
}
CONVERSION_TABLE: dict[tuple[str, str], float] = {
    # Velocity
    ("m/s",  "km/h"): 3.6,
    ("km/h", "m/s"):  1 / 3.6,
    # Force
    ("N",    "kgf"):  1 / 9.81,
    ("kgf",  "N"):    9.81,
    # Pressure
    ("pa",   "psi"):  1 / 6894.76,
    ("psi",  "pa"):   6894.76,
}

### COLOR SYSTEM

def _intclip(val: int, lower: int, upper: int) -> int:
    if val <= lower:
        return lower
    elif val >= upper:
        return upper
    return val
def _validatehex(hexcode: str) -> str:
    """Validates a hexstring for colors. If invalid, returns `#000000`"""
    hexcode = hexcode[1:7]
    hexchars = "abcdef0123456789"
    if len(hexcode) != 6:
        return "#000000"
    
    for char in hexcode.lower():
        if char not in hexchars:
            return "#000000"
        
    return "#" + hexcode
    
class _BaseColor:
    "Base class for color data types."
    def __init__(self, colorname: str):
        self.colorname = colorname
    
    def __str__(self):
        return self.colorname
    def __repr__(self):
        return self.colorname
    
class RGB(_BaseColor):
    "RGB color data type."
    def __init__(self, colorname: str, r: int, g: int, b: int):
        super().__init__(colorname)
        self.r = _intclip(r, 0, 255)
        self.g = _intclip(g, 0, 255)
        self.b = _intclip(b, 0, 255)
        
    # add dunder methods
    
    @property
    def values(self) -> tuple[int, int, int]:
        return (self.r, self.g, self.b)
    
    def toHex(self) -> str:
        """Converts the RGB color to a hexadecimal color code in the format "#RRGGBB"."""
        return f"#{self.r:02x}{self.g:02x}{self.b:02x}"
    def toCMYK(self) -> tuple[int, int, int, int]:
        """Converts the RGB color to CMYK color values."""
        r_scaled = self.r / 255
        g_scaled = self.g / 255
        b_scaled = self.b / 255
        
        k = 1 - max(r_scaled, g_scaled, b_scaled)
        if k == 1:
            return (0, 0, 0, 100)
        
        c = (1 - r_scaled - k) / (1 - k)
        m = (1 - g_scaled - k) / (1 - k)
        y = (1 - b_scaled - k) / (1 - k)
        
        return (int(c * 100), int(m * 100), int(y * 100), int(k * 100)) 
class HEX(_BaseColor):
    "Hex color data type."
    def __init__(self, colorname: str, hexcode: str):
        super().__init__(colorname)
        self.hexcode = _validatehex(hexcode)

    @property
    def values(self) -> str:
        return self.hexcode
    
    def toRGB(self) -> tuple[int, int, int]:
        """Converts the hexadecimal color code to RGB color values."""
        hexcode = self.hexcode.lstrip('#')
        r = int(hexcode[0:2], 16)
        g = int(hexcode[2:4], 16)
        b = int(hexcode[4:6], 16)
        return (r, g, b)
    def toCMYK(self) -> tuple[int, int, int, int]:
        """Converts the hexadecimal color code to CMYK color values."""
        r, g, b = self.toRGB()
        r_scaled = r / 255
        g_scaled = g / 255
        b_scaled = b / 255
        
        k = 1 - max(r_scaled, g_scaled, b_scaled)
        if k == 1:
            return (0, 0, 0, 100) # Pure black
        
        c = (1 - r_scaled - k) / (1 - k)
        m = (1 - g_scaled - k) / (1 - k)
        y = (1 - b_scaled - k) / (1 - k)
        
        return (int(c * 100), int(m * 100), int(y * 100), int(k * 100))   
class CMYK(_BaseColor):
    "CMYK color data type."
    def __init__(self, colorname: str, c: int, m: int, y: int, k: int):
        super().__init__(colorname)
        self.c = _intclip(c, 0, 100)
        self.m = _intclip(m, 0, 100)
        self.y = _intclip(y, 0, 100)
        self.k = _intclip(k, 0, 100)

    @property
    def values(self) -> tuple[int, int, int, int]:
        return (self.c, self.m, self.y, self.k)

    def toRGB(self) -> tuple[int, int, int]:
        """Converts the CMYK color values to RGB color values."""
        r = 255 * (1 - self.c / 100) * (1 - self.k / 100)
        g = 255 * (1 - self.m / 100) * (1 - self.k / 100)
        b = 255 * (1 - self.y / 100) * (1 - self.k / 100)
        return (int(r), int(g), int(b))
    def toHex(self) -> str:
        """Converts the CMYK color values to a hexadecimal color code in the format "#RRGGBB"."""
        r, g, b = self.toRGB()
        return f"#{r:02x}{g:02x}{b:02x}"
    
