"""
The Classical Mechanics module for `AWPC` `UniPhys`

This module contains resources for calculations and simulations for Classical Mechanics. 
"""

import math

from commons.utils import xColorText
from commons.types import Quantity, UNITS
from commons.constants import EARTH_G, C

def Torque(MomentArmDistance: float, Force: float) -> Quantity:
    """Returns a `torque` quantity in newtonmeters from moment arm distance in meters and force in newtons."""
    return Quantity((MomentArmDistance * Force), UNITS["Nm"])
def GearRatio(DrivingGearTeethCount: int, DrivenGearTeethCount: int) -> str:
    """Returns the gear ratio from the driving gear's teeth count and the driven gear's teeth count."""
    Ratio = DrivenGearTeethCount / DrivingGearTeethCount
    if Ratio > 1:
        return f"{Ratio} - {xColorText('Speed-', 'red')} - {xColorText('Torque+', 'green')}"
    elif Ratio < 1:
        return f"{Ratio} - {xColorText('Speed+', 'green')} - {xColorText('Torque-', 'red')}"
    else:
        return f"{Ratio} - Same Speed - Same Torque"

def AngularVelocityR(RPM: float) -> Quantity:
    """Returns angular velocity from RPM in radians/s"""
    return Quantity((RPM * math.pi / 30), UNITS["Rad"])
def AngularVelocityD(RPM: float) -> Quantity:
    """Returns angular velocity from RPM in degrees/s"""
    return Quantity(math.degrees((RPM * math.pi / 30)), UNITS["Deg"])

def KineticEnergy(Mass: float, Velocity: float) -> Quantity:
    """Returns the kinetic energy from mass in kgs and velocity in m/s"""
    return Quantity((0.5 * Mass * Velocity**2), UNITS["J"])
def PotentialEnergy(Mass: float, Height: float, Gravity: float | None = EARTH_G.value) -> Quantity:
    """Returns the potential energy of a mass. Gravity is defaulted to 9.8m /s^2"""
    return Quantity(Mass * Gravity * Height, UNITS["J"])

def EinsteinMassEnergyEquivalence(Mass: float) -> Quantity:
    return Quantity((Mass * C ** 2), UNITS["J"])

