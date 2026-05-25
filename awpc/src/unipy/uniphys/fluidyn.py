"""
The Fluid dynamics module for `AWPC` `UniPhys`

This module contains resources for calculations and simulations for Fluid Dynamics. 
"""

def reynolds_number(velocity, characteristic_length, kinematic_viscosity):
    """
    Calculate the Reynolds number for a given flow.

    Parameters:
    velocity (float): The velocity of the fluid (m/s).
    characteristic_length (float): The characteristic length of the flow (m).
    kinematic_viscosity (float): The kinematic viscosity of the fluid (m^2/s).

    Returns:
    float: The Reynolds number.
    """
    return (velocity * characteristic_length) / kinematic_viscosity