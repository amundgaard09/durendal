"""
The `AWPC` `UniFlight` module provides a collection of functions and classes for performing calculations and simulations related to flight dynamics, aerodynamics, and propulsion.
"""

from awpc.src.package.commons.utils import xColorText
from awpc.src.package.commons.types import Quantity, UNITS
from awpc.src.package.commons.constants import MACH

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
