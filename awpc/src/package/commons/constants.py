"""
This module contains all the physical constants used in the `AWPC` library, such as the gravitational constant, speed of light, and various planetary parameters. 
The constants are stored as instances of the `PhysicalConstant` class, which includes the value, unit, and name of the constant.
"""

from awpc.src.package.commons.types import PhysicalConstant, UNITS

G       = PhysicalConstant(6.674e-11, UNITS["GCONST"], "Gravitational Constant")
C       = PhysicalConstant(299792458, UNITS["m/s"],    "Speed of Light")
AU      = PhysicalConstant(1.496e+11, UNITS["m"],      "Astronomical Unit")
MACH    = PhysicalConstant(343,       UNITS["m/s"],    "Speed of Sound at sea level")

EARTH_G = PhysicalConstant(9.8,       UNITS["m/s^2"],  "Surface Gravity of the Earth")
MOON_G  = PhysicalConstant(1.62,      UNITS["m/s^2"],  "Surface Gravity of the Moon")
MARS_G  = PhysicalConstant(3.71,      UNITS["m/s^2"],  "Surface Gravity of Mars")
SUN_G   = PhysicalConstant(274,       UNITS["m/s^2"],  "Surface Gravity of the Sun")

EARTH_M = PhysicalConstant(5.972e+24, UNITS["kg"],     "Mass of the Earth")
MOON_M  = PhysicalConstant(7.342e+22, UNITS["kg"],     "Mass of the Moon")
MARS_M  = PhysicalConstant(6.390e+23, UNITS["kg"],     "Mass of Mars")
SUN_M   = PhysicalConstant(1.989e+30, UNITS["kg"],     "Mass of the Sun")

EARTH_R = PhysicalConstant(6.371e+6,  UNITS["m"],      "Radius of the Earth")
MOON_R  = PhysicalConstant(1.737e+6,  UNITS["m"],      "Radius of the Moon")
MARS_R  = PhysicalConstant(3.390e+6,  UNITS["m"],      "Radius of Mars")
SUN_R   = PhysicalConstant(6.957e+8,  UNITS["m"],      "Radius of the Sun")
