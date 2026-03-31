"""The complete UNIMATH Library from AmundWorks - Iteration I"""

import math, time
from typing_extensions import Literal

class ImpossibleTriangleError(Exception):
    def __init__(self):
        super().__init__("The angles of a triangle cant be anything else than 180 degrees!")

class ContinuousPID:
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

def Quadratic(A: float, B: float, C: float) -> tuple[float]:
    """Solves quadratic equations and returns x-values in a tuple."""
    if A == 0:
        return ValueError("Invalid quadratic equation! A cannot be 0.")
    D = B**2 - 4*A*C
    if D > 0:
        x1 = (-B - math.sqrt(D)) / (2 * A)
        x2 = (-B + math.sqrt(D)) / (2 * A)
        return (x1, x2)
    
    elif D == 0:
        x1 = -B / (2 * A)
        return (x1)
    
    else:
        return None

def SineRule(
    Sides: list[float | None],
    Angles: list[float | None],
    AngleMeasurementMode: Literal["Degrees", "Radians"]
) -> list[list[float], list[float]] | None:
    """
    Sine Rule

    Formula: A / sin(a) = B / sin(b) = C / sin(c)

    Return Format: [Angles:[A, B, C], Sides:[A, B, C]]
    """
   
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

    ### Return None if no reference ratio could be established, meaning there is not enough information to solve the triangle.
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
    Returns a tuple of the three angles in degrees, in the order of AngleA, AngleB, AngleC 
    
    Formula: AngleA = arccos((B^2 + C^2 - A^2) / (2BC))
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

    Args:
        LenghtA (float):
        LenghtB (float):
        LenghtC (float):

    Returns:
        Area (float):
    """
    S = (LengthA + LengthB + LengthC) / 2
    return math.sqrt(S * (S - LengthA) * (S - LengthB) * (S - LengthC))

def D2R(Degrees: float) -> float:
    return Degrees / 180 * math.pi
def R2D(Radians: float) -> float:
    return Radians / math.pi * 180
