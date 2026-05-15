"""
The `AWPC` Color System module.

This module includes terminal text coloring tools and color data classes such as `RGB`, `HEX` and `CMYK`.
"""

from __future__ import annotations

def _intclip(val: int, lower: int, upper: int) -> int:
    if val <= lower:
        return lower
    elif val >= upper:
        return upper
    return val

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

def xColorText(Text: str, Color: str) -> str:
    """Returns the given text in the given color using `ANSI` escape codes. If the color is not found, it returns the text without coloring."""
    Text = str(Text)
    ANSI = ANSI_COLORS.get(Color.lower(), '\033[0m')
    return ANSI + Text + '\033[0m'

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
        self._r = r
        self._g = g
        self._b = b
        
    # add dunder methods
    
    @property
    def r(self) -> int:
        """Getter: Returns the red value."""
        return self._r
    @r.setter
    def r(self, new_value: int) -> None:
        """Setter: Clips and assigns the new red value."""
        self._r = _intclip(new_value, 0, 255) 
    @property
    def g(self) -> int:
        """Getter: Returns the green value."""
        return self._g
    @g.setter
    def g(self, new_value: int) -> None:
        """Setter: Clips and assigns the new green value."""
        self._g = _intclip(new_value, 0, 255)
    @property
    def b(self) -> int:
        """Getter: Returns the blue value."""
        return self._b
    @b.setter
    def b(self, new_value: int) -> None:
        """Setter: Clips and assigns the new blue value."""
        self._b = _intclip(new_value, 0, 255)
            
    
    def toHex(self) -> HEX:
        """Converts the RGB color to a hexadecimal color code in the format "#RRGGBB"."""
        return HEX(None, f"#{self.r:02x}{self.g:02x}{self.b:02x}")
    def toCMYK(self) -> CMYK:
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
        
        return CMYK(None, int(c * 100), int(m * 100), int(y * 100), int(k * 100)) 
class HEX(_BaseColor):
    "Hex color data type."
    def __init__(self, colorname: str, hexcode: str):
        super().__init__(colorname)
        self.hexcode = _validatehex(hexcode)

    @property
    def r(self) -> int:
        """Getter: Returns the red value as an integer (0-255)."""
        return int(self.hexcode[1:3], 16)
    @r.setter
    def r(self, new_hex: str) -> None:
        """Setter: Updates the red component in the hex string."""
        self.hexcode = _validatehex("#" + new_hex + self.hexcode[3:])
    @property
    def g(self) -> int:
        """Getter: Returns the green value as an integer (0-255)."""
        return int(self.hexcode[3:5], 16)
    @g.setter
    def g(self, new_hex: str) -> None:
        """Setter: Updates the green component in the hex string."""
        self.hexcode = _validatehex(self.hexcode[:3] + new_hex + self.hexcode[5:])
    @property
    def b(self) -> int:
        """Getter: Returns the blue value as an integer (0-255)."""
        return int(self.hexcode[5:7], 16)
    @b.setter
    def b(self, new_hex: str) -> None:
        """Setter: Updates the blue component in the hex string."""
        self.hexcode = _validatehex(self.hexcode[:5] + new_hex)
           
    
    def toRGB(self) -> RGB:
        """Converts the hexadecimal color code to RGB color values."""
        hexcode = self.hexcode.lstrip('#')
        r = int(hexcode[0:2], 16)
        g = int(hexcode[2:4], 16)
        b = int(hexcode[4:6], 16)
        return RGB(None, r, g, b)
    def toCMYK(self) -> CMYK:
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
        
        return CMYK(None, int(c * 100), int(m * 100), int(y * 100), int(k * 100))   
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

    def toRGB(self) -> RGB:
        """Converts the CMYK color values to RGB color values."""
        r = 255 * (1 - self.c / 100) * (1 - self.k / 100)
        g = 255 * (1 - self.m / 100) * (1 - self.k / 100)
        b = 255 * (1 - self.y / 100) * (1 - self.k / 100)
        return RGB(None, int(r), int(g), int(b))
    def toHex(self) -> HEX:
        """Converts the CMYK color values to a hexadecimal color code in the format "#RRGGBB"."""
        r, g, b = self.toRGB()
        return HEX(None, f"#{r:02x}{g:02x}{b:02x}")
    
