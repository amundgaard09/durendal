"""
The `AWPC` `UniSpace` module provides a collection of functions and classes for performing calculations related to orbital mechanics, astrodynamics, and space physics.
"""

import math

from awpc.src.types.phys_dtypes import Quantity, UNITS
from awpc.src.commons.constants import G, EARTH_M, EARTH_R

def OrbitalPeriod(SemiMajorAxis: float, M: float, m: float) -> Quantity:
    return Quantity((2 * math.pi * math.sqrt(SemiMajorAxis ** 3 / (G * (M + m)))), UNITS["S"])
def OrbitalVelocity(OrbitalRadius: float = EARTH_R, Mass: float = EARTH_M) -> Quantity:
    return Quantity((math.sqrt((G * Mass) / OrbitalRadius)), UNITS["m/s"])
def EscapeVelocity(Radius: float = EARTH_R, Mass: float = EARTH_M) -> Quantity:
    return Quantity((math.sqrt(2) * OrbitalVelocity(Radius, Mass)), UNITS["m/s"])

def GravitationalForce(Mass1: float, Mass2: float, Distance: float) -> Quantity:
    return Quantity((G * Mass1 * Mass2 / Distance ** 2), UNITS["N"])
def SurfaceGravity(Mass: float, Radius: float) -> Quantity:
    return Quantity((G * Mass / Radius ** 2), UNITS["m/s^2"])

def TsiolkovskyRocketEquation(ExhaustVelocity: float, InitialMass: float, FinalMass: float) -> Quantity:
    return Quantity((ExhaustVelocity * math.log(InitialMass / FinalMass)), UNITS["Δv"])
