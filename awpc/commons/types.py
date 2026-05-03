"""
This module contains the base classes for the unit system used in the `AWPC` library, including `Unit`, `Quantity`, and `PhysicalConstant`. 
It also includes a conversion table for converting between different units of measurement. 
The unit system is designed to unify units of measurement along with their dimensions (e.g. length, weight, etc.) and to allow for easy conversion between compatible units.
"""

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

class BaseColor:
    "Base class for color data types."
    def __init__(self, colorname: str):
        self.colorname = colorname
    
class RGB(BaseColor):
    "RGB color data type."
    def __init__(self, colorname: str, r: int, g: int, b: int):
        super().__init__(colorname)
        self.r = r
        self.g = g
        self.b = b
        
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
            return (0, 0, 0, 100) # Pure black
        
        c = (1 - r_scaled - k) / (1 - k)
        m = (1 - g_scaled - k) / (1 - k)
        y = (1 - b_scaled - k) / (1 - k)
        
        return (int(c * 100), int(m * 100), int(y * 100), int(k * 100)) 
class HexColor(BaseColor):
    "Hex color data type."
    def __init__(self, colorname: str, hexcode: str):
        super().__init__(colorname)
        self.hexcode = hexcode

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
class CMYK(BaseColor):
    "CMYK color data type."
    def __init__(self, colorname: str, c: int, m: int, y: int, k: int):
        super().__init__(colorname)
        self.c = c
        self.m = m
        self.y = y
        self.k = k

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