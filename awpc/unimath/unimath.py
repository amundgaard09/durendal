"""
The UniMath function library for the `AWPC` library. 
This library contains functions for various mathematical calculations, including geometry, algebra, calculus, and more. The functions are designed to be easy to use and understand, with clear input and output formats. 
The library is still in development and may contain some unstable functions that are not yet fully tested.
"""

import math, time, sympy
import matplotlib.pyplot as mpl

from typing import Literal
from awpc.utils.utils import *

class ContinuousPIDController:
    def __init__(self, kp, ki, kd, setpoint=0):
        self.kp = kp  # Proportional gain
        self.ki = ki  # Integral gain
        self.kd = kd  # Derivative gain
        self.setpoint = setpoint

        self.integral = 0
        self.prev_error = 0
        self.prev_time = time.time()

    def update(self, measured_value):
        now = time.time()
        dt = now - self.prev_time          # Elapsed time

        error = self.setpoint - measured_value

        # P term
        P = self.kp * error

        # I term — integrates error over time
        self.integral += error * dt
        I = self.ki * self.integral

        # D term — rate of error change
        derivative = (error - self.prev_error) / dt if dt > 0 else 0
        D = self.kd * derivative

        # Store state for next iteration
        self.prev_error = error
        self.prev_time = now

        return P + I + D  # Control output u(t)

def _plotXY(XVals: list[float], YVals: list[float]) -> None:
    """Initialize a plot where `x[idx]` and `y[idx]` are coordinate pairs of a function."""
    mpl.plot(XVals, YVals, color='red', linestyle='--')
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

    SinA = math.sin(math.radians(a))
    SinB = math.sin(math.radians(b))
    SinC = math.sin(math.radians(c))
    
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
    """Calculates the missing side of a right-angled triangle using either normal or reverse pythagoras."""
    
    if (A, B, C).count(None) > 1:
        return None
    
    if A is None:
        A = math.sqrt(C**2 - B**2)
    elif B is None:
        B = math.sqrt(C**2 - A**2)
    elif C is None:
        C = math.sqrt(A**2 + B**2)
    
    return f"A: {A}, B: {B}, C: {C}"

def SineRule(
    Sides: list[float | None],
    Angles: list[float | None],
    AngleMeasurementMode: Literal["Degrees", "Radians"]
    ) -> list[list[float], list[float]] | None:
    """
    Sine Rule

    Formula:
    `A / sin(a) = B / sin(b) = C / sin(c)`

    Return Format: [Angles: [A, B, C], Sides: [A, B, C]]
    """
    ### VERY UNSTABLE!
    angles_rad = []
    for angle in Angles:
        if angle is not None and AngleMeasurementMode == "Degrees":
            angles_rad.append(math.radians(angle))
        else:
            angles_rad.append(angle)

    known_angle_indices = [i for i in range(3) if angles_rad[i] is not None]
    if len(known_angle_indices) == 2:
        missing = next(i for i in range(3) if angles_rad[i] is None)
        angles_rad[missing] = math.pi - sum(angles_rad[i] for i in known_angle_indices)

    ReferenceRatio = None
    
    for idx in range(3):
        if Sides[idx] is not None and angles_rad[idx] is not None:
            ReferenceRatio = Sides[idx] / math.sin(angles_rad[idx])
            break
        
    if ReferenceRatio is None:
        return None

    for idx in range(3):
        if Sides[idx] is None and angles_rad[idx] is not None:
            Sides[idx] = ReferenceRatio * math.sin(angles_rad[idx])
        elif angles_rad[idx] is None and Sides[idx] is not None:
            value = Sides[idx] / ReferenceRatio
            if not -1 <= value <= 1:
                return None
            asin_val = math.asin(value)
            known_sum = sum(a for a in angles_rad if a is not None)
            
            ### Check for the ambiguous case of the sine rule, where there may be two possible angles that satisfy the equation
            if math.pi - asin_val + known_sum <= math.pi:
                angles_rad[idx] = math.pi - asin_val
            else:
                angles_rad[idx] = asin_val

    if AngleMeasurementMode == "Degrees":
        Angles_out = [math.degrees(a) if a is not None else None for a in angles_rad]
    else:
        Angles_out = angles_rad

    return [Angles_out, Sides]
def CosineRule(LengthA: float, LengthB: float, AngleA: float) -> float:
    return math.sqrt(LengthA ** 2 + LengthB ** 2 - ((2 * LengthA * LengthB) * math.cos(math.radians(AngleA))))
def ReverseCosineRule(LengthA: float, LengthB: float, LengthC: float) -> tuple[float]:
    """ 
    Returns a tuple of the three angles in degrees, in the order of AngleA, AngleB, and AngleC.
    
    Formula::

        AngleA = math.arccos((B**2 + C**2 - A**2) / (2 * B * C))
        
    """

    return (
        math.degrees(math.acos((LengthB ** 2 + LengthC ** 2 - LengthA ** 2) / (2 * LengthB * LengthC))),  # AngleA
        math.degrees(math.acos((LengthC ** 2 + LengthA ** 2 - LengthB ** 2) / (2 * LengthC * LengthA))),  # AngleB
        math.degrees(math.acos((LengthA ** 2 + LengthB ** 2 - LengthC ** 2) / (2 * LengthA * LengthB)))   # AngleC
    )

def SASArea(LengthA: float, LengthB: float, AngleC: float) -> float:
    return (0.5 * LengthA * LengthB * math.sin(math.radians(AngleC)))
def HeronsFormula(LengthA: float, LengthB: float, LengthC: float) -> float:
    """
    Returns the area of a triangle from the side lengths.
    Formula::

        S: float = (LengthA + LengthB + LengthC) / 2
        Area: float = math.sqrt(S * (S - LengthA) * (S - LengthB) * (S - LengthC))

    """
    S = (LengthA + LengthB + LengthC) / 2
    return math.sqrt(S * (S - LengthA) * (S - LengthB) * (S - LengthC))

def D2R(Degrees: float) -> float:
    """Return radians from degrees."""
    return Degrees / 180 * math.pi
def R2D(Radians: float) -> float:
    """Return degrees from radians."""
    return Radians / math.pi * 180

def Slope(x1: float, y1: float, x2: float, y2: float) -> float:
    """Returns the slope of a line from two points `(x1, y1)` and `(x2, y2)`"""
    return f"slope = {(y2 - y1) / (x2 - x1)}"
def Distance(x1: float, y1: float, x2: float, y2: float) -> float:
    """Return the distance between two points `(x1, y1)` and `(x2, y2)`"""
    return math.sqrt((x2-x1)**2 + (y2-y1)**2)
def Derivative(Function: str, x: float | None = None, h: float = 1e-5) -> float:
    """Returns f'(x) if x is not given, else returns the numerical derivative of the function at the given x-value using the definition of the derivative."""
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
    yv = a*xv**2 + b*xv + c

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
        x1 = (-B - math.sqrt(D)) / (2 * A)
        x2 = (-B + math.sqrt(D)) / (2 * A)
        return f"x1: {x1}, x2: {x2}"
    
    elif D == 0:
        x1 = -B / (2 * A)
        return f"x: {x1}"
    else: 
        return ColorText('No real solutions', 'red')
def QuadraticEvaluation(a: float, b: float, c: float, x: float) -> str:
    return f"{a}x^2 + {b}x + {c} = {a*x**2 + b*x + c}"

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
        print(ColorText(string, 'green' if result == 0 else 'red'))
        
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

def PrimeFactorize(N: int) -> list[int]:
    """Returns the prime factorization of a number as a list of prime factors."""
    factors = []
    divisor = 2
    
    while N >= 2:
        if N % divisor == 0:
            factors.append(divisor)
            N //= divisor
        else:
            divisor += 1
            
    return factors
