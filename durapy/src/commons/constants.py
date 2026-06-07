"""
The `DuraPy` Constants Library

This module contains all the physical constants used in the `DuraPy` library, such as the gravitational constant, speed of light, and various planetary parameters. 
The constants are stored as instances of the `PhysicalConstant` class, which includes the value, unit, and name of the constant.
"""

# Alpha - A α, Beta - B β, Gamma - Γ γ, Delta - Δ δ,  Epsilon - E ε, Zeta - Z ζ, Eta - H η, 
# Theta - Θ θ, Iota - I ι, Kappa - K κ, Lambda - Λ λ, Mu - M μ,      Nu - N ν,   Xi - Ξ ξ,  Omicron - O ο, 
# Pi - Π π,    Rho - P ρ,  Sigma - Σ σ ς, Tau - T τ,  Ypsilon - Y υ, Phi - Φ φ,  Chi - X χ, Psi - Ψ ψ, Omega - Ω ω

from durapy.src.unipy.uniphys.phys_dtypes import PhysicalConstant, UNITS

# Mathematical Constants (Numerical/Unitless Constants - NCONST)
I       = PhysicalConstant(1j,                 UNITS["NCONST"], "Imaginary Unit - sqrt(-1)")
E       = PhysicalConstant(2.718281828459045,  UNITS["NCONST"], "Eulers Number")
PI      = PhysicalConstant(3.141592653589793,  UNITS["NCONST"], "Pi - π")
TAU     = PhysicalConstant(6.283185307179586,  UNITS["NCONST"], "Archimedes' Constant - τ - (AKA 2 * PI)")
INF     = PhysicalConstant(float('inf'),       UNITS["NCONST"], "Positive Infinity")
NINF    = PhysicalConstant(float('-inf'),      UNITS["NCONST"], "Negative Infinity")
GOLDEN  = PhysicalConstant(1.618033988749895,  UNITS["NCONST"], "The Golden Ratio - φ,")
EULMAS  = PhysicalConstant(0.5772156649015329, UNITS["NCONST"], "The Euler-Mascheroni Constant")
FSTRUCT = PhysicalConstant(7.2973525693e-03,   UNITS["NCONST"], "Fine-Structure Constant") 
   
# Gravitational Constants
G       = PhysicalConstant(6.674e-11,       UNITS["GCONST"], "Gravitational Constant")

# Energy Constants
PLANCK  = PhysicalConstant(6.62607015e-34,  UNITS["J*s"], "Planck's Constant")
PLANCKR = PhysicalConstant(1.054571817e-34, UNITS["J*s"], "Reduced Planck Constant")

# Speed Constants
C       = PhysicalConstant(299792458,       UNITS["m/s"], "Speed of Light")
MACH    = PhysicalConstant(343,             UNITS["m/s"], "Speed of Sound at sea level")

# Length Constants
PLANCKL = PhysicalConstant(1.616255e-35,    UNITS["m"], "Planck Length") 
BOHR_R  = PhysicalConstant(5.291772109e-11, UNITS["m"], "The Bohr Radius")
ASTUNIT = PhysicalConstant(1.496e+11,       UNITS["m"], "Astronomical Unit")
LIGHTYR = PhysicalConstant(9.461e+15,       UNITS["m"], "Light year")
PARSEC  = PhysicalConstant(3.086e+16,       UNITS["m"], "Parsec")

# Mass Constants
ELECTRON_MASS = PhysicalConstant(9.1093837015e-31,  UNITS["kg"], "Electron Mass")
PROTON_MASS   = PhysicalConstant(1.67262192369e-27, UNITS["kg"], "Proton Mass")
NEUTRON_MASS  = PhysicalConstant(1.67492749804e-27, UNITS["kg"], "Neutron Mass")

# Celestial Body Surface Gravities
EARTH_G = PhysicalConstant(9.8,       UNITS["m/s²"], "Surface Gravity of the Earth")
MOON_G  = PhysicalConstant(1.62,      UNITS["m/s²"], "Surface Gravity of the Moon")
MARS_G  = PhysicalConstant(3.71,      UNITS["m/s²"], "Surface Gravity of Mars")
SUN_G   = PhysicalConstant(274,       UNITS["m/s²"], "Surface Gravity of the Sun")

# Celestial Body Masses
EARTH_M = PhysicalConstant(5.972e+24, UNITS["kg"],   "Mass of the Earth")
MOON_M  = PhysicalConstant(7.342e+22, UNITS["kg"],   "Mass of the Moon")
MARS_M  = PhysicalConstant(6.390e+23, UNITS["kg"],   "Mass of Mars")
SUN_M   = PhysicalConstant(1.989e+30, UNITS["kg"],   "Mass of the Sun")

# Celestial Body Radii
EARTH_R = PhysicalConstant(6.371e+6,  UNITS["m"],    "Radius of the Earth")
MOON_R  = PhysicalConstant(1.737e+6,  UNITS["m"],    "Radius of the Moon")
MARS_R  = PhysicalConstant(3.390e+6,  UNITS["m"],    "Radius of Mars")
SUN_R   = PhysicalConstant(6.957e+8,  UNITS["m"],    "Radius of the Sun")

# TODO Sort and implement all units 
HUBBLE           = PhysicalConstant(70.0,               UNITS["km/s/prsc"],  "Hubble Constant")
#BOLTZMANN        = PhysicalConstant(1.380649e-23,      UNITS["J/K"],        "Boltzmann Constant")         # Relates the average relative kinetic energy of particles in a gas with the thermodynamic temperature of the gas.
#GAS_CONSTANT     = PhysicalConstant(8.314462618,       UNITS["J/(mol*K)"],  "Universal Gas Constant")     # Work performed by one mole of a gas during a temperature change of 1 Kelvin at constant pressure.
#AVOGADRO         = PhysicalConstant(6.02214076e+23,    UNITS["1/mol"],      "Avogadro Constant")          # Number of constituent particles (usually atoms or molecules) contained in one mole of a substance.
#STEFAN_BOLTZMANN = PhysicalConstant(5.670374419e-08,   UNITS["W/(m²*K^4)"], "Stefan-Boltzmann Constant")  # Constant of proportionality in the Stefan-Boltzmann law relating total energy radiated per unit surface area of a black body.
#WIEN             = PhysicalConstant(2.897771955e-03,   UNITS["m*K"],        "Wien Displacement Constant") # Relationship between the thermodynamic temperature of a blackbody and the wavelength of its peak radiation.
#VAC_PERMITTIVITY = PhysicalConstant(8.8541878128e-12,  UNITS["F/m"],        "Vacuum Permittivity")        # Capability of a vacuum to permit electric field lines; also known as the electric constant.
#VAC_PERMEABILITY = PhysicalConstant(1.25663706127e-06, UNITS["N/A²"],       "Vacuum Permeability")        # Measure of the resistance encountered when forming a magnetic field in a vacuum; also known as the magnetic constant.
VAC_IMPEDANCE    = PhysicalConstant(376.730313412,     UNITS["Ω"],          "Vacuum Impedance")           # Ratio of the magnitudes of the electric and magnetic fields in an electromagnetic wave traveling through a vacuum.
#COULOMB          = PhysicalConstant(8.9875517923e+09,  UNITS["N*m²/C²"],    "Coulomb Constant")           # Proportionality constant used in electrostatics equations, equal to 1 / (4pi * epsilon_0).
#FARADAY          = PhysicalConstant(96485.33212,       UNITS["C/mol"],      "Faraday Constant")           # Total electric charge carried by one mole of electrons.
#JOSEPHSON        = PhysicalConstant(483597.8484e+09,   UNITS["Hz/V"],       "Josephson Constant")         # Constant relating the potential difference across a Josephson junction to the frequency of the alternating current.
#RYDBERG          = PhysicalConstant(10973731.56816,    UNITS["1/m"],        "Rydberg Constant")           # Limiting value of the highest wavenumber of any photon that can be emitted from an atom.
