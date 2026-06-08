"""
The DuraPy STEM Python Package from Durendal Engineering.

DuraPy is the complete collection of all open-source Python projects from Durendal. 
"""

from .src.unipy.unialgo import unialgo
from .src.unipy.uniCLI import uniCLI
from .src.unipy.unicogni import unicogni
from .src.unipy.unicrypt import unicrypt
from .src.unipy.uniflight import uniflight
from .src.unipy.uniops import uniops
from .src.unipy.unipower import unipower
from .src.unipy.unispace import unispace
from .src.unipy.univiz import univiz

from .src.unipy.unimath import unimath
from .src.unipy.unimath import linalg_dtypes

from .src.unipy.uniphys.phys_dtypes import (Unit, UNITS, PhysicalConstant, Quantity)
from .src.unipy.uniphys import (
    mechanics, 
    acoustics, 
    astrophys, 
    electromags, 
    fluidyn, 
    quantum, 
    thermodyn, 
    nuclear
)

from .src.commons import exceptions, constants
from .src.types.color_dtypes import (
    RGB, 
    CMYK, 
    HEX, 
    color_text
)

__all__ = ["src"]
__version__ = "0.0.1.7"
