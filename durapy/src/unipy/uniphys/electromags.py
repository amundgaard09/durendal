"""
The `AWPC` Electromagnetics module for `UniPhys`

This module provides resources for calculations related to charged particles, electric and magnetic fields, optics and other related branches.
"""

from durapy.src.types.color_dtypes import x_color_text as ct
from durapy.src.commons.constants import PLANCK, INF, C

__WAVLN_UV_SPEC: dict[tuple[float, float], str] = {
    (10, 13.5): f"{ct('EUV', 'Violet')}", 
    (13.5,100): f"{ct('DUV', 'Violet')}", 
    (100, 280): f"{ct('UVC', 'Violet')}", 
    (280, 315): f"{ct('UVB', 'Violet')}", 
    (315, 390): f"{ct('UVA', 'Violet')}", 
}
__WAVLN_VSBL_SPEC: dict[tuple[float, float], str] = {
    (390, 450): f"{ct('Violet', 'violet')}", 
    (450, 495): f"{ct('Blue',   'blue')}", 
    (495, 570): f"{ct('Green',  'green')}", 
    (570, 590): f"{ct('Yellow', 'yellow')}", 
    (590, 620): f"{ct('Orange', 'orange')}", 
    (620, 750): f"{ct('Red',    'red')}", 
}

_WAVLN_EM_SPEC: dict[tuple[float, float], str | dict] = {
    (0, 0.01): "Gamma-ray",
    (0.01, 10): "X-Ray",
    (10, 400): __WAVLN_UV_SPEC,
    (400, 700): __WAVLN_VSBL_SPEC,
    (700, 1e6): "Infrared Light",
    (1e7, 1e10): "Micro Wave",
    (1e10, INF): "Radio Wave",
}

def _spectrum_label(λ: float, spectrum_map: dict[tuple[float, float], str | dict]) -> str:
    """Return the spectrum label (e.g. `Radio Wave` or `X-Ray`) by checking recursively for wavelength `λ` in `spectrum_map`."""
    for (low, high), value in spectrum_map.items():
        if low <= λ < high:
            if isinstance(value, dict):
                return _spectrum_label(λ, value)
            return value
    raise ValueError(f"Wavelength {λ!r} is out of range for this spectrum map")

def λ(Hz: float) -> float:
    """Return wavelength `λ` from `Hertz`."""
    return C / Hz
def hz(λ: float) -> float:
    """Return `Hertz` from wavelength `λ`."""
    return C / λ*1e9

def ems(λ: float) -> tuple[str, float, str]:
    """
    Get the part of the electromagnetic spectrum the wavelength `λ` sits in, as well as the hertz.
    """
    label = _spectrum_label(λ, _WAVLN_EM_SPEC)
    Hz = hz(λ)
    
    return label, Hz, f'{label} - {Hz} Hz'

def photon_energy_λ(λ: float) -> float:
    """Calculate the energy of a photon with wavelength `λ`."""
    return PLANCK * hz(λ)
def photon_energy_hz(Hz: float) -> float:
    """Calculate the energy of a photon with frequency `Hz`."""
    return PLANCK * Hz
def photon_energy_ev_λ(λ: float) -> float:
    """Calculate the energy of a photon with wavelength `λ` in electron volts."""
    return photon_energy_λ(λ) / 1.60218e-19
def photon_energy_ev_hz(Hz: float) -> float:
    """Calculate the energy of a photon with frequency `Hz` in electron volts."""
    return photon_energy_hz(Hz) / 1.60218e-19
