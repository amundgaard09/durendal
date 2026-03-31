
import math

def TsiolkovskyRocketEquation(ExhaustVelocity: float, InitialMass: float, Finalmass: float) -> float:
    return ExhaustVelocity * math.log(InitialMass/Finalmass)
