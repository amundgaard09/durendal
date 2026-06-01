"""
The complete DuraPy Package.
"""

from .src.unipy.uniCLI import uniCLI
from .src.unipy.unialgo import unialgo
from .src.unipy.unicrypt import unicrypt
from .src.unipy.uniflight import uniflight
from .src.unipy.unimath import unimath
from .src.unipy.uniops import uniops
from .src.unipy.uniphys import mechanics, acoustics, astrophys, electromags, fluidyn, quantum, thermodyn, nuclear
from .src.unipy.unipower import unipower
from .src.unipy.unispace import unispace
from .src.unipy.univiz import univiz

from .src.commons import exceptions, constants
from .src.types import color_dtypes, linalg_dtypes, phys_dtypes

__all__ = ["src"]
__version__ = "0.0.1.2"
