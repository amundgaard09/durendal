"""
The Acoustic Physics module for `AWPC` `UniPhys`

This module contains resources for calculations and simulations for Acoustic Physics. 
"""

from awpc.src.types.phys_dtypes import Quantity, UNITS
from awpc.src.commons.constants import MACH
import math

def sound_speed(temperature: float, γ: float = 1.4, molar_mass: float = 0.02897) -> float:
    """Calculate the speed of sound in a gas given the temperature, adiabatic index (gamma), and molar mass."""
    R = 8.314  # Universal gas constant in J/(mol*K)
    return ((γ * R * temperature) / molar_mass) ** 0.5
def sound_pressure_level(pressure: float, reference_pressure: float = 20e-6) -> float:
    """Calculate the sound pressure level (SPL) in decibels (dB) given the pressure and reference pressure."""
    return 20 * math.log10(pressure / reference_pressure)
def intensity_level(intensity: float, reference_intensity: float = 1e-12) -> float:
    """Calculate the intensity level in decibels (dB) given the intensity and reference intensity."""
    return 10 * math.log10(intensity / reference_intensity)

def frequency_from_wavelength(wavelength: float, speed_of_sound: float = MACH) -> float:
    """Calculate the frequency of a sound wave given its wavelength and the speed of sound."""
    return speed_of_sound / wavelength
def wavelength_from_frequency(frequency: float, speed_of_sound: float = MACH) -> float:
    """Calculate the wavelength of a sound wave given its frequency and the speed of sound."""
    return speed_of_sound / frequency

def decibel_to_intensity(decibel: float, reference_intensity: float = 1e-12) -> float:
    """Convert a sound level in decibels (dB) to intensity given a reference intensity."""
    return reference_intensity * (10 ** (decibel / 10))
def decibel_to_pressure(decibel: float, reference_pressure: float = 20e-6) -> float:
    """Convert a sound level in decibels (dB) to pressure given a reference pressure."""
    return reference_pressure * (10 ** (decibel / 20))

def intensity_to_decibel(intensity: float, reference_intensity: float = 1e-12) -> float:
    """Convert an intensity to decibels (dB) given a reference intensity."""
    return 10 * math.log10(intensity / reference_intensity)
def pressure_to_decibel(pressure: float, reference_pressure: float = 20e-6) -> float:
    """Convert a pressure to decibels (dB) given a reference pressure."""
    return 20 * math.log10(pressure / reference_pressure)

def sound_intensity(pressure: float, speed_of_sound: float = MACH, density: float = 1.225) -> float:
    """Calculate the sound intensity given the pressure, speed of sound, and density of the medium."""
    return (pressure ** 2) / (speed_of_sound * density)
def sound_pressure(intensity: float, speed_of_sound: float = MACH, density: float = 1.225) -> float:
    """Calculate the sound pressure given the intensity, speed of sound, and density of the medium."""
    return (intensity * speed_of_sound * density) ** 0.5

