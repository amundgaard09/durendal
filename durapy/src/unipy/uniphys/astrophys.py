"""
The Astrophysics module for `AWPC` `UniPhys`

This module contains resources for calculations and simulations for Astrophysics. 
"""

# Alpha - A α, Beta - B β, Gamma - Γ γ, Delta - Δ δ,  Epsilon - E ε, Zeta - Z ζ, Eta - H η, 
# Theta - Θ θ, Iota - I ι, Kappa - K κ, Lambda - Λ λ, Mu - M μ,      Nu - N ν,   Xi - Ξ ξ,  Omicron - O ο, 
# Pi - Π π,    Rho - P ρ,  Sigma - Σ σ ς, Tau - T τ,  Ypsilon - Y υ, Phi - Φ φ,  Chi - X χ, Psi - Ψ ψ, Omega - Ω ω

import math
from durapy.src.unipy.uniphys.phys_dtypes import Quantity, UNITS
from durapy.src.commons.constants import G, C, PI, EARTH_M, EARTH_R, HUBBLE 

def SchwarzschildRadius(M: float) -> Quantity:
    return Quantity(((2 * G * M) / C * C), UNITS["m"])

def Redshift(λobs: float, λrest: float) -> Quantity:
    return Quantity(((λobs - λrest) / λrest), UNITS["nm"])

def OrbitalPeriod(SemiMajorAxis: float, M: float, m: float) -> Quantity:
    return Quantity((2 * PI * math.hypot(0, SemiMajorAxis ** 3 / (G * (M + m)))), UNITS["S"])
def OrbitalVelocity(OrbitalRadius: float = EARTH_R, Mass: float = EARTH_M) -> Quantity:
    return Quantity((math.hypot(0, (G * Mass) / OrbitalRadius)), UNITS["m/s"])
def EscapeVelocity(Radius: float = EARTH_R, Mass: float = EARTH_M) -> Quantity:
    return Quantity((math.hypot(0, 2) * OrbitalVelocity(Radius, Mass)), UNITS["m/s"])

def NewtonsGravitation(Mass1: float, Mass2: float, Distance: float) -> Quantity:
    return Quantity((G * Mass1 * Mass2 / Distance ** 2), UNITS["N"])
def SurfaceGravity(Mass: float, Radius: float) -> Quantity:
    return Quantity((G * Mass / Radius ** 2), UNITS["m/s^2"])

def TsiolkovskyRocketEquation(ExhaustVelocity: float, InitialMass: float, FinalMass: float) -> Quantity:
    if FinalMass > InitialMass:
        return Quantity(0, UNITS["Δv"])
    
    return Quantity((ExhaustVelocity * math.log(InitialMass / FinalMass)), UNITS["Δv"])

def HubbleLaw(Distance: float) -> Quantity:
    return Quantity((HUBBLE * Distance), UNITS["m/s"])