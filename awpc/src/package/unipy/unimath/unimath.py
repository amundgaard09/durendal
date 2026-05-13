"""
The UniMath function library for the `AWPC` library. 
This module provides a collection of functions for performing various mathematical calculations, 
including geometry, algebra, calculus, and more.
"""

import sympy, matplotlib.pyplot as mpl

from math import sin, asin, cos, acos, sqrt

from typing import Literal
from commons.color_dtypes import xColorText
from commons.math_dtypes import SquareMatrix, D3Vector
from commons.constants import PI
from commons.exceptions import ImpossibleTriangleError

def _plotXY(XVals: list[float], YVals: list[float]) -> None:
    """Initialize a plot where `x[idx]` and `y[idx]` are coordinate pairs of a function."""
    mpl.plot(XVals, YVals, color='red', linestyle='-', marker='o')
    mpl.xlabel('X')
    mpl.ylabel('Y')
    mpl.axhline(0, color='black')
    mpl.axvline(0, color='black')
    mpl.show()
    
    return

def TriExtrapolate(a: float, b: float, c: float, A: float | None = None, B: float | None = None, C: float | None = None) -> str:
    """Extrapolate the sides of a triangle from the AAAS case (3x Angle + 1x Side)"""

    if sum((a, b, c)) != 180:
        raise ImpossibleTriangleError

    SinA = sin(D2R)(a)
    SinB = sin(D2R(b))
    SinC = sin(D2R(c))
    
    if A is not None:
        B = (A * SinB) / SinA
        C = (A * SinC) / SinA
        
    elif B is not None:
        A = (B * SinA) / SinB
        C = (B * SinC) / SinB
        
    elif C is not None:
        A = (C * SinA) / SinC
        B = (C * SinB) / SinC
    
    Area = HeronsFormula(A, B, C)
    
    return f"""Area: {Area} - Sides: A: {A}, B: {B}, C: {C} - Sin({a}) = {SinA}, Sin({b}) = {SinB}, Sin({c}) = {SinC}"""
def Pythagoras(A: float | None = None, B: float | None = None, C: float | None = None) -> str:
    """
    Calculates the missing side of a right-angled triangle using either normal or reverse pythagoras.
    Formula: `A² + B² = C²` for normal, and `A² = C² - B²` or  `B² = C² - A²` for reverse.
    
    The function can take in any two sides and will return the missing side, as well as the values of all three sides. If more than one side is missing, the function will return `None`.
    If no sides are missing, the function will return the values of all three sides.
    """
    
    if (A, B, C).count(None) > 1:
        return None
    
    if A is None:
        A = sqrt(C**2 - B**2)
    elif B is None:
        B = sqrt(C**2 - A**2)
    elif C is None:
        C = sqrt(A**2 + B**2)
    
    return f"A: {A}, B: {B}, C: {C}"

def SineRule(
    Sides: list[float | None],
    Angles: list[float | None],
    AngleMeasurementMode: Literal["Degrees", "Radians"]
    ) -> list[list[float], list[float]] | None:
    """
    The Sine Rule calculation function. Takes in 

    Formula:
    `A / sin(a)` = `B / sin(b)` = `C / sin(c)`

    Return Format: [Angles: [A, B, C], Sides: [A, B, C]]
    """
    
    ### VERY UNSTABLE!
    
    angles_rad = []
    ReferenceRatio = None
    
    # Convert angles to radians if they are in degrees, and keep them as is if they are already in radians. If an angle is None, keep it as None.
    for angle in Angles:
        if angle is not None and AngleMeasurementMode == "Degrees":
            angles_rad.append(D2R(angle))
        else:
            angles_rad.append(angle)

    known_angle_indices = [i for i in range(3) if angles_rad[i] is not None]
    
    # If two angles are known, calculate the third angle using the fact that the sum of angles in a triangle is 180 degrees (or π radians).
    if len(known_angle_indices) == 2:
        missing = next(i for i in range(3) if angles_rad[i] is None)
        angles_rad[missing] = PI - sum(angles_rad[i] for i in known_angle_indices)
    
    # Find the first known side and angle to establish the reference ratio for the Sine Rule
    for idx in range(3):
        if Sides[idx] is not None and angles_rad[idx] is not None:
            ReferenceRatio = Sides[idx] / sin(angles_rad[idx])
            break
    
    # If the reference couldn't be established, return None
    if ReferenceRatio is None:
        return None

    # Loop through the sides and angles to calculate the missing values using the Sine Rule
    for idx in range(3):
        if Sides[idx] is None and angles_rad[idx] is not None:
            Sides[idx] = ReferenceRatio * sin(angles_rad[idx])
        elif angles_rad[idx] is None and Sides[idx] is not None:
            value = Sides[idx] / ReferenceRatio
            if not -1 <= value <= 1:
                return None
            asin_val = asin(value)
            known_sum = sum(a for a in angles_rad if a is not None)
            
            # Check for the ambiguous case of the sine rule, where there may be two possible angles that satisfy the equation
            if PI - asin_val + known_sum <= PI:
                angles_rad[idx] = PI - asin_val
            else:
                angles_rad[idx] = asin_val

    # Return in specified unit
    if AngleMeasurementMode == "Degrees":
        Angles_out = [R2D(a) if a is not None else None for a in angles_rad]
    else:
        Angles_out = angles_rad

    return [Angles_out, Sides]
def CosineRule(LengthA: float, LengthB: float, AngleA: float) -> float:
    return sqrt(LengthA ** 2 + LengthB ** 2 - ((2 * LengthA * LengthB) * cos(D2R(AngleA))))
def ReverseCosineRule(LengthA: float, LengthB: float, LengthC: float) -> tuple[float]:
    """ 
    Returns a tuple of the three angles in degrees, in the order of AngleA, AngleB, and AngleC.
    
    Formula:
        Angle A = arccos( ( B² + C² - A² ) / ( 2 * B * C ) )
    """

    return (
        R2D(acos((LengthB ** 2 + LengthC ** 2 - LengthA ** 2) / (2 * LengthB * LengthC))),  # AngleA
        R2D(acos((LengthC ** 2 + LengthA ** 2 - LengthB ** 2) / (2 * LengthC * LengthA))),  # AngleB
        R2D(acos((LengthA ** 2 + LengthB ** 2 - LengthC ** 2) / (2 * LengthA * LengthB)))   # AngleC
    )

def SASArea(LengthA: float, LengthB: float, AngleC: float) -> float:
    """
    Returns the area of a triangle from two sides and the included angle.
    Formula: `Area = 0.5 * LengthA * LengthB * sin(AngleC)` where AngleC is in degrees.
    """
    return (0.5 * LengthA * LengthB * sin(D2R(AngleC)))
def HeronsFormula(LengthA: float, LengthB: float, LengthC: float) -> float:
    """
    Returns the area of a triangle from the side lengths.
    Formula::

        S: float = (LengthA + LengthB + LengthC) / 2
        Area: float = math.sqrt(S * (S - LengthA) * (S - LengthB) * (S - LengthC))

    """
    S = (LengthA + LengthB + LengthC) / 2
    return sqrt(S * (S - LengthA) * (S - LengthB) * (S - LengthC))

def D2R(Degrees: float) -> float:
    """Return radians from degrees."""
    return Degrees / 180 * PI
def R2D(Radians: float) -> float:
    """Return degrees from radians."""
    return Radians / PI * 180

def Slope(x1: float, y1: float, x2: float, y2: float) -> str:
    """Returns the slope of a line from two points `(x1, y1)` and `(x2, y2)`"""
    return f"Slope = {(y2 - y1) / (x2 - x1)}"
def Distance(x1: float, y1: float, x2: float, y2: float) -> float:
    """Return the distance between two points `(x1, y1)` and `(x2, y2)`"""
    return sqrt((x2-x1)**2 + (y2-y1)**2)
def Derivative(Function: str, x: float | None = None, h: float = 1e-5) -> float:
    """Returns `f'(x)` if `x` is not given, else returns the numerical derivative of the function at the given x-value using the definition of the derivative."""
    x_sym = sympy.symbols('x')
    f = sympy.sympify(Function)
    if x is None:
        return sympy.diff(f, x_sym)
    else:
        return (f.subs(x_sym, x + h) - f.subs(x_sym, x - h)) / (2 * h)

def LineIntersection(m1: float, b1: float, m2: float, b2: float) -> str:
    """"Return the point of intersection of two lines in the form of `(x, y)`"""
    x = (b2 - b1) / (m1 - m2)
    y = m1*x + b1
    return f"Intersection Point: ({x:.3f}, {y:.3f})"
def LineFromPoints(x1: float, y1: float, x2: float, y2: float) -> str:
    """Returns the equation of a line in the form of `y = mx + b` from two points `(x1, y1)` and `(x2, y2)`."""
    m = (y2 - y1) / (x2 - x1)
    b = y1 - m * x1
    return f"y = {m}x + {b}"
def LinearZero(m: float, b: float) -> float:
    """Find the x-value where the line `y = mx + b` crosses the x-axis"""
    return -b / m
def LinearEvaluation(m: float, b: float, x: float) -> str:
    return f"{m}x + {b} = {m*x + b}"    

def QuadraticVertex(a: float, b: float, c: float) -> str:
    """Returns the vertex (aka the minimum/maximum point) of a quadratic function in the form of `(x, y)`."""
    xv = -b / (2*a)
    yv = QuadraticEvaluation(a, b, c, xv).split('= ')[-1]

    return f"Vertex: ({xv}, {yv}) - {'Minimum' if a > 0 else 'Maximum' if a < 0 else 'Linear'}"
def QuadraticNumRoots(a: float, b: float, c: float) -> int:
    """Returns the number of roots of a quadratic function based on the discriminant."""
    D = b**2 - 4*a*c
    return 2 if D > 0 else 1 if D == 0 else 0
def QuadraticSolutions(A: float, B: float, C: float) -> str:
    """Solves quadratic equations and returns x-values in a tuple."""
    if A == 0:
        return ValueError("Invalid quadratic equation! A cannot be 0.")
    D = B**2 - 4*A*C
    if D > 0:
        x1 = (-B - sqrt(D)) / (2 * A)
        x2 = (-B + sqrt(D)) / (2 * A)
        return f"x1: {xColorText(x1, 'green')}, x2: {xColorText(x2, 'green')}"
    
    elif D == 0:
        x1 = -B / (2 * A)
        return f"x: {xColorText(x1, 'green')}"
    else: 
        return xColorText('No real solutions', 'red')
def QuadraticFactorizedForm(a: float, b: float, c: float) -> str:
    """Returns the factorized form of a quadratic function in the form of `a(x - x1)(x - x2)` where `x1` and `x2` are the roots of the function."""
    D = b**2 - 4*a*c
    if D > 0:
        x1 = (-b - sqrt(D)) / (2 * a)
        x2 = (-b + sqrt(D)) / (2 * a)
        return f"{a}(x - {x1})(x - {x2})"
    
    elif D == 0:
        x1 = -b / (2 * a)
        return f"{a}(x - {x1})^2"
    else: 
        return xColorText('No real solutions', 'red')
def QuadraticZeros(a: float, b: float, c: float) -> str:
    """Returns the x-values where the quadratic function crosses the x-axis."""
    D = b**2 - 4*a*c
    if D > 0:
        x1 = (-b - sqrt(D)) / (2 * a)
        x2 = (-b + sqrt(D)) / (2 * a)
        return f"Zeros: {xColorText((x1, 0), 'green')}, {xColorText((x2, 0), 'green')}"
    
    elif D == 0:
        x1 = -b / (2 * a)
        return f"Zero: {xColorText((x1, 0), 'green')}"
    else: 
        return xColorText('No real zeros', 'red')
def QuadraticEvaluation(a: float, b: float, c: float, x: float) -> str:
    return f"{a}x^2 + {b}x + {c} = {a*x**2 + b*x + c}"

def CubicVertex(a: float, b: float, c: float, d: float) -> str:
    """Returns the vertex (aka the minimum/maximum point) of a cubic function in the form of `(x, y)`."""
    x = sympy.symbols('x')
    f = sympy.sympify(f"{a}*x**3 + {b}*x**2 + {c}*x + {d}")
    df = sympy.diff(f, x)
    critical_points = sympy.solve(df, x)
    
    vertices = []
    for point in critical_points:
        y = f.subs(x, point)
        vertices.append((point, y))
    
    return f"Vertices: {xColorText(vertices, 'green' if all(v[1].is_real for v in vertices) else 'red')}"
def CubicNumRoots(a: float, b: float, c: float, d: float) -> int:
    """Returns the number of roots of a cubic function based on the discriminant."""
    D = 18*a*b*c*d - 4*b**3*d + b**2*c**2 - 4*a*c**3 - 27*a**2*d**2
    return 3 if D > 0 else 2 if D == 0 else 1
def CubicSolutions(a: float, b: float, c: float, d: float) -> str:
    """Returns the roots of a cubic function in a tuple."""
    x = sympy.symbols('x')
    f = sympy.sympify(f"{a}*x**3 + {b}*x**2 + {c}*x + {d}")
    solutions = sympy.solve(f, x)
    return f"Solutions: {xColorText(solutions, 'green' if all(sol.is_real for sol in solutions) else 'red')}"
def CubicZeros(a: float, b: float, c: float, d: float) -> str:
    """Returns the x-values where the cubic function crosses the x-axis."""
    x = sympy.symbols('x')
    f = sympy.sympify(f"{a}*x**3 + {b}*x**2 + {c}*x + {d}")
    zeros = sympy.solve(f, x)
    return f"Zeros: {xColorText(zeros, 'green' if all(z.is_real for z in zeros) else 'red')}"
def CubicEvaluation(a: float, b: float, c: float, d: float, x: float) -> tuple[str, float]:
    """Cubic Evaluation function"""
    result = a*x**3 + b*x**2 + c*x + d
    return (f"f({x}) = {a}x^3 + {b}x^2 + {c}x^+ {d} = {result}", result)
def CubicEvaluationBruteForce(a: float, b: float, c: float, d: float, LowerBound: int, UpperBound: int) -> str:
    """Brute Force evaluation of a third-degree polynomial. The function checks all evaluations from `LowerBound` to `UpperBound` and highlights roots as green, as well as plotting the given function."""
    xvals, yvals, roots = [], [], []
    
    for x in range(int(LowerBound), int(UpperBound+1)):
        string, result = CubicEvaluation(a, b, c, d, x)
        xvals.append(x)
        yvals.append(result)
        roots.append(x) if result == 0 else None
        print(xColorText(string, 'green' if result == 0 else 'red'))
        
    print(f"Roots: {roots}")
    _plotXY(xvals, yvals)
    return

### UNSTABLE - ALPHA - DO NOT USE
def TangentFormula(Function1: str, Function2: str) -> list[str]:
    """Returns the tangent(s) between two functions by finding the points where the derivatives are equal and then calculating the slope of the tangent line at those points."""
    x = sympy.symbols('x')
    f1 = sympy.sympify(Function1)
    f2 = sympy.sympify(Function2)

    df1 = sympy.diff(f1, x)
    df2 = sympy.diff(f2, x)

    slope_eq = sympy.Eq(df1, df2)
    tangent_points = sympy.solve(slope_eq, x)

    tangents = []
    for idx, point in enumerate(tangent_points, 1):
        string = f"Tangent {idx} - point: {point} - y: {f1.subs(x, point)} - slope: {df1.subs(x, point)}"
        tangents.append(string) 

    return tangents

def PrimeFactorize(Number: int) -> list[int]:
    """Returns the prime factorization of a number as a list of prime factors."""
    Factors = []
    Divisor = 2
    
    while Number >= 2:
        if Number % Divisor == 0:
            Factors.append(Divisor)
            Number //= Divisor
        else:
            Divisor += 1
            
    return Factors

def Rx(θ: float) -> SquareMatrix:
    θ = D2R(θ)
    return SquareMatrix([
        [1, 0,       0     ], 
        [0, cos(θ), -sin(θ)], 
        [0, sin(θ),  cos(θ)]])
def Ry(θ: float) -> SquareMatrix:
    θ = D2R(θ)
    return SquareMatrix([
        [cos(θ),  0,  sin(θ)], 
        [0,       1,  0     ], 
        [-sin(θ), 0,  cos(θ)]])
def Rz(θ: float) -> SquareMatrix:
    θ = D2R(θ)
    return SquareMatrix([
        [cos(θ), -sin(θ), 0], 
        [sin(θ),  cos(θ), 0], 
        [0,       0,      1]])
    
def D3Vector_rotate(V: D3Vector, x: float, y: float, z: float):
    """Rotates a 3D vector V by angles x, y, and z around the x, y, and z axes respectively."""
        
    R = (Rz(z) @ (Ry(y) @ Rx(x)))
    newVec = R @ V
    
    return newVec

### - TODO: Add more functions for various mathematical calculations, such as:
### - More functions for geometry, such as area and volume calculations for various shapes, surface area calculations, and more.
### - More functions for algebra, such as polynomial expansion, factorization, and more.
### - More functions for calculus, such as integration, limits, and more.
### - More functions for linear algebra, such as matrix operations, determinants, eigenvalues, and more.
### - More functions for number theory, such as GCD, LCM, modular arithmetic, and more.
### - More functions for engineering and physics, such as kinematics equations, projectile motion calculations, work and energy calculations, and more.