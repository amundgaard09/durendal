
from typing import Tuple

# Alpha - A α, Beta - B β, Gamma - Γ γ, Delta - Δ δ,  Epsilon - E ε, Zeta - Z ζ, Eta - H η, 
# Theta - Θ θ, Iota - I ι, Kappa - K κ, Lambda - Λ λ, Mu - M μ,      Nu - N ν,   Xi - Ξ ξ,  Omicron - O ο, 
# Pi - Π π,    Rho - P ρ,  Sigma - Σ σ ς, Tau - T τ,  Ypsilon - Y υ, Phi - Φ φ,  Chi - X χ, Psi - Ψ ψ, Omega - Ω ω

_REG: dict[Tuple[float, ...], str] = {
    # Canonical Key Format: (L, M, T, I, θ, N, J) - Length, Mass, Time, Current, Temperature, Amount of Substance & Luminous Intensity
    (0, 0, 0, 0, 0, 0, 0): "Dimensionless",
    
    # Base Dimensions
    (1, 0, 0, 0, 0, 0, 0): "Length",
    (0, 1, 0, 0, 0, 0, 0): "Mass",
    (0, 0, 1, 0, 0, 0, 0): "Time",
    (0, 0, 0, 1, 0, 0, 0): "Current",
    (0, 0, 0, 0, 1, 0, 0): "Temperature",
    
    # Kinematics & Mechanics
    (2, 0, 0, 0, 0, 0, 0): "Area",
    (3, 0, 0, 0, 0, 0, 0): "Volume",
    (1, 0, -1, 0, 0, 0, 0): "Velocity",
    (1, 0, -2, 0, 0, 0, 0): "Acceleration",
    (1, 1, -2, 0, 0, 0, 0): "Force",
    (-1, 1, -2, 0, 0, 0, 0): "Pressure",
    (2, 1, -2, 0, 0, 0, 0): "Energy",
    (2, 1, -3, 0, 0, 0, 0): "Power",
    (0, 0, -1, 0, 0, 0, 0): "Frequency",
    
    # Electromagnetism
    (0, 0, 1, 1, 0, 0, 0):   "ElectricCharge",
    (2, 1, -3, -1, 0, 0, 0): "Voltage",
    (2, 1, -3, -2, 0, 0, 0): "Resistance",
    (-2, -1, 4, 2, 0, 0, 0): "ElectricCapacitance",
    (0, 1, -2, -1, 0, 0, 0): "MagneticFluxDensity",
}

class _Dimension:
    _REGISTRY = _REG
    
    def __init__(
            self, 
            L: float = 0, 
            M: float = 0, 
            T: float = 0, 
            I: float = 0, 
            θ: float = 0, 
            N: float = 0, 
            J: float = 0, 
            name: str = None
        ):
        
        self._exponents: Tuple[float, ...] = (float(L), float(M), float(T), float(I), float(θ), float(N), float(J))
        
        if name:
            self._REGISTRY[self._exponents] = name

    @property
    def exponents(self) -> Tuple[float, ...]:
        return self._exponents

    @property
    def name(self) -> str:
        return self._REGISTRY.get(self._exponents, self._build_exponent_string())

    def _build_exponent_string(self) -> str:
        symbols = ['L', 'M', 'T', 'I', 'θ', 'N', 'J']
        terms = [f"{sym}^{ext}" if ext != 1 else sym 
                 for sym, ext in zip(symbols, self._exponents) if ext != 0]
        return " * ".join(terms) if terms else "Dimensionless"

    def __mul__(self, other: '_Dimension') -> '_Dimension':
        if not isinstance(other, _Dimension):
            return NotImplemented
        new_exp = tuple(a + b for a, b in zip(self._exponents, other._exponents))
        return _Dimension(*new_exp)

    def __truediv__(self, other: '_Dimension') -> '_Dimension':
        if not isinstance(other, _Dimension):
            return NotImplemented
        new_exp = tuple(a - b for a, b in zip(self._exponents, other._exponents))
        return _Dimension(*new_exp)

    def __pow__(self, power: float) -> '_Dimension':
        new_exp = tuple(x * power for x in self._exponents)
        return _Dimension(*new_exp)

    def __eq__(self, other: object) -> bool:
        if not isinstance(other, _Dimension):
            return False
        return self._exponents == other._exponents

    def __hash__(self) -> int:
        return hash(self._exponents)

    def __repr__(self) -> str:
        return f"Dimension({self.name})"

class Unit:
    def __init__(self, dimension: _Dimension, symbol: str, name: str):
        self._dimension = dimension
        self._symbol = symbol
        self._name = name

    @property
    def dimension(self) -> _Dimension:
        return self._dimension

    @property
    def symbol(self) -> str:
        return self._symbol

    @property
    def name(self) -> str:
        return self._name
    
    def __mul__(self, other: 'Unit') -> 'Unit':
        if not isinstance(other, Unit):
            return NotImplemented
        
        return Unit(
            dimension=self._dimension * other._dimension,
            symbol=f"({self._symbol}*{other._symbol})",
            name=f"{self._name}_{other._name}"
        )
    def __truediv__(self, other: 'Unit') -> 'Unit':
        if not isinstance(other, Unit):
            return NotImplemented
            
        return Unit(
            dimension=self._dimension / other._dimension,
            symbol=f"({self._symbol}/{other._symbol})",
            name=f"{self._name}_per_{other._name}"
        )
    def __pow__(self, power: float) -> 'Unit':
        return Unit(
            dimension=self._dimension ** power,
            symbol=f"{self._symbol}^{power}",
            name=f"{self._name}^{power}"
        )
    def __eq__(self, other: object) -> bool:
        if not isinstance(other, Unit):
            return False
        return self._dimension == other._dimension
    def __repr__(self) -> str:
        return f"Unit({self._symbol}, Type: {self._dimension.name})"

# 1. Base Dimensions
Dimensionless = _Dimension(     name="Dimensionless")
Length        = _Dimension(L=1, name="Length")
Mass          = _Dimension(M=1, name="Mass")
Time          = _Dimension(T=1, name="Time")
Current       = _Dimension(I=1, name="Current")
Temperature   = _Dimension(θ=1, name="Temperature")

# 2. Derived Mechanical Dimensions
Area          = _Dimension(L=2,             name="Area")
Volume        = _Dimension(L=3,             name="Volume")
Velocity      = _Dimension(L=1, T=-1,       name="Velocity")
Delta_V       = _Dimension(L=1, T=-1,       name="Delta_V")
Acceleration  = _Dimension(L=1, T=-2,       name="Acceleration")
Force         = _Dimension(L=1, M=1, T=-2,  name="Force")
Energy        = _Dimension(L=2, M=1, T=-2,  name="Energy")
Power         = _Dimension(L=2, M=1, T=-3,  name="Power")
Pressure      = _Dimension(L=-1, M=1, T=-2, name="Pressure")
Torque        = _Dimension(L=2, M=1, T=-2,  name="Torque")
Frequency     = _Dimension(T=-1,            name="Frequency")

# 3. Derived Electrical Dimensions
ElectricCharge      = _Dimension(T=1, I=1,             name="ElectricCharge")
Voltage             = _Dimension(L=2, M=1, T=-3, I=-1, name="Voltage")
Resistance          = _Dimension(L=2, M=1, T=-3, I=-2, name="Resistance")
ElectricCapacitance = _Dimension(L=-2, M=-1, T=4, I=2, name="ElectricCapacitance")
MagneticFluxDensity = _Dimension(M=1, T=-2, I=-1,      name="MagneticFluxDensity")  
    
    
    