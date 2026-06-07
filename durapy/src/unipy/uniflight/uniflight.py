"""
The `AWPC` `UniFlight` module provides a collection of functions and classes for performing calculations and simulations related to flight dynamics, aerodynamics, and propulsion.
"""

from durapy.src.types.color_dtypes import color_text
from durapy.src.unipy.uniphys.phys_dtypes import Quantity, UNITS
from durapy.src.commons.constants import MACH

def T2W_ratio(Thrust: float, Weight: float) -> str:
    """Thrust to Weight ratio calculator. Ensure consistent units!"""
    Ratio = Thrust / Weight
    return f"Ratio: {color_text(f'{Ratio}', 'green' if Ratio > 1 else 'red' if Ratio != 1 else 'yellow')}" 
def mach_number(Velocity: float, SpeedOfSound: float | None = MACH) -> str:
    """Mach Number Calulator. Speed of sound is defaulted to 343 m/s. Ensure consistent units!"""
    mach = Velocity / SpeedOfSound
    label = ('SUBSONIC' if mach < 1 else 'TRANSONIC' if abs(mach - 1) < 0.01 else 'SUPERSONIC' if mach < 5 else 'HYPERSONIC' if mach < 10 else 'HIGH-HYPERSONIC')
    color = ('red'      if mach < 1 else 'yellow'    if mach == 1            else 'green'      if mach < 5 else 'blue'       if mach < 10 else 'violet')
    return f"Ratio: {color_text(f'{mach} - {label}', color)}"
                                
def dynamic_pressure(Velocity: float, AirDensity: float | None = 1.225) -> Quantity:
    return Quantity(0.5 * Velocity ** 2 * AirDensity, UNITS["Pa"])

def lift_equation(LiftCoefficient: float, DynamicPressure: float, ReferenceArea: float) -> Quantity:
    return Quantity(LiftCoefficient * DynamicPressure * ReferenceArea, UNITS["N"])
def drag_equation(DragCoefficient: float, DynamicPressure: float, ReferenceArea: float) -> Quantity:
    return Quantity(DragCoefficient * DynamicPressure * ReferenceArea, UNITS["N"])
