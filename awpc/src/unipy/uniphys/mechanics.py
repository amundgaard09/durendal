"""
The Classical Mechanics module for `AWPC` `UniPhys`

This module contains resources for calculations and simulations for Classical Mechanics. 
"""

from awpc.src.types.color_dtypes import xColorText as ColorText
from awpc.src.types.phys_dtypes import Quantity, UNITS
from awpc.src.commons.constants import EARTH_G, PI, C 
from awpc.src.unipy.unimath import D2R

def Torque(MomentArmDistance: float, Force: float) -> Quantity:
    """Returns a `torque` quantity in newtonmeters from moment arm distance in meters and force in newtons."""
    return Quantity((MomentArmDistance * Force), UNITS["Nm"])
def GearRatio(DrivingGearTeethCount: int, DrivenGearTeethCount: int) -> str:
    """Returns the gear ratio from the driving gear's teeth count and the driven gear's teeth count."""
    Ratio = DrivenGearTeethCount / DrivingGearTeethCount
    if Ratio > 1:
        return f"{Ratio} - {ColorText('Speed-', 'red')} - {ColorText('Torque+', 'green')}"
    elif Ratio < 1:
        return f"{Ratio} - {ColorText('Speed+', 'green')} - {ColorText('Torque-', 'red')}"
    else:
        return f"{Ratio} - Same Speed - Same Torque"

def AngularVelocityR(RPM: float) -> Quantity:
    """Returns angular velocity from RPM in radians/s"""
    return Quantity((RPM * PI / 30), UNITS["rad"])
def AngularVelocityD(RPM: float) -> Quantity:
    """Returns angular velocity from RPM in degrees/s"""
    return Quantity(D2R((RPM * PI / 30)), UNITS["deg"])

def KineticEnergy(Mass: float, Velocity: float) -> Quantity:
    """Returns the kinetic energy from mass in kgs and velocity in m/s"""
    return Quantity((0.5 * Mass * Velocity**2), UNITS["J"])
def PotentialEnergy(Mass: float, Height: float, Gravity: float | None = EARTH_G.value) -> Quantity:
    """Returns the potential energy of a mass. Gravity is defaulted to 9.8m /s^2"""
    return Quantity(Mass * Gravity * Height, UNITS["J"])

def EinsteinMassEnergyEquivalence(Mass: float) -> Quantity:
    return Quantity((Mass * C * C), UNITS["J"])

