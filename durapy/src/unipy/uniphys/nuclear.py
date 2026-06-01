"""
The Nuclear Physics module for `AWPC` `UniPhys`

This module contains resources for calculations and simulations for Nuclear Physics. 
"""

from durapy.src.commons.constants import E

def RadioactiveDecay(InitialQuantity: float, DecayConstant: float, Time: float) -> float:
    """Returns the remaining quantity of a radioactive substance after a given time, based on its initial quantity and decay constant."""
    return InitialQuantity * (E ** (-DecayConstant * Time))
def HalfLife(DecayConstant: float) -> float:
    """Returns the half-life of a radioactive substance based on its decay constant."""
    return 0.693 / DecayConstant
def DecayConstant(HalfLife: float) -> float:
    """Returns the decay constant of a radioactive substance based on its half-life."""
    return 0.693 / HalfLife
def Activity(Quantity: float, DecayConstant: float) -> float:
    """Returns the activity of a radioactive substance based on its quantity and decay constant."""
    return DecayConstant * Quantity
def MeanLifetime(DecayConstant: float) -> float:
    """Returns the mean lifetime of a radioactive substance based on its decay constant."""
    return 1 / DecayConstant
def DecayEnergy(MassDefect: float) -> float:
    """Returns the energy released in a nuclear decay based on the mass defect."""
    return MassDefect * E
def BindingEnergy(MassDefect: float) -> float:
    """Returns the binding energy of a nucleus based on the mass defect."""
    return MassDefect * E
def MassDefect(MassOfProtons: float, MassOfNeutrons: float, MassOfNucleus: float) -> float:
    """Returns the mass defect of a nucleus based on the mass of its protons, neutrons, and the nucleus itself."""
    return (MassOfProtons + MassOfNeutrons) - MassOfNucleus
def DecayRate(InitialQuantity: float, DecayConstant: float) -> float:
    """Returns the decay rate of a radioactive substance based on its initial quantity and decay constant."""
    return DecayConstant * InitialQuantity

