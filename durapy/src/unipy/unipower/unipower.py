"""
The UniPower function library for the `DuraPy` library. 
This library contains functions for electrical calculations and simulations. The functions are designed to be easy to use and understand, with clear input and output formats. 
The library is still in development and may contain some unstable functions that are not yet fully tested.
"""

import math

from types import MappingProxyType
from typing_extensions import Literal
from durapy.src.types.color_dtypes import ANSI_COLORS
from durapy.src.unipy.uniphys.phys_dtypes import (
    Quantity,
    UNITS
)

from durapy.src.commons.exceptions import (
    MissingParameters, 
    InconsistencyError, 
    InvalidColors
)

BANDS = MappingProxyType({
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
})
MULTIPLIERS = MappingProxyType({
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
})
TOLERANCES = MappingProxyType({
    "brown":  1,
    "red":    2,
    "green":  0.5,
    "blue":   0.25,
    "violet": 0.1,
    "gray":   0.05,
    "gold":   5,
    "silver": 10,
})

def OhmsLaw(V: float | None = None, I: float | None = None, R: float | None = None) -> str:
    """
    Ohms Law calculation for Voltage, Current, and Resistivity. \n
    Formulas:
    >>> V = I * R \n
    >>> I = V / R \n 
    >>> R = V / I \n 
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
    return Quantity((2 * math.pi * Hertz * Inductance), UNITS["Ohm"])
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
        totalCapacitance = sum(cap[0] for cap in caps)
        VoltLimit = min([cap[1] for cap in caps])
        
    elif ConnectionType == "series":
        totalCapacitance = 1 / sum(1/cap[0] for cap in caps)
        VoltLimit = sum([cap[1] for cap in caps])   
        
    else:
        raise ValueError("Connection type must be 'parallel' or 'series'")

    return f"Total Capacitance: {totalCapacitance}, Volt Limit: {VoltLimit}, Total ESR: {TotalESR(caps, ConnectionType)}"
