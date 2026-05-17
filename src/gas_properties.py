"""Gas thermodynamic properties for turbofan nozzle analysis."""

import math
from dataclasses import dataclass


@dataclass
class GasProperties:
    """Container for gas thermodynamic properties."""
    gamma: float       # specific heat ratio (Cp/Cv)
    R: float           # specific gas constant [J/(kg·K)]
    Cp: float          # specific heat at constant pressure [J/(kg·K)]
    Cv: float          # specific heat at constant volume [J/(kg·K)]
    name: str = "air"


def get_air_properties(T: float = 300.0) -> GasProperties:
    """Return standard air properties at a given temperature.

    Args:
        T: static temperature in Kelvin.

    Returns:
        GasProperties for dry air.
    """
    pass


def get_combustion_gas_properties(FAR: float, T: float = 1200.0) -> GasProperties:
    """Return approximate properties for combustion gases given fuel-air ratio.

    Args:
        FAR: fuel-to-air ratio (mass).
        T: static temperature in Kelvin.

    Returns:
        GasProperties for hot combustion gases.
    """
    pass


def calculate_density(
    pressure_kpa: float,
    temperature_k: float,
    gas_constant: float,
) -> float:
    """Compute gas density from the ideal gas law.

    Args:
        pressure_kpa: static pressure [kPa]. Must be > 0.
        temperature_k: static temperature [K]. Must be > 0.
        gas_constant: specific gas constant R [J/(kg·K)]. Must be > 0.

    Returns:
        Density [kg/m³].

    Raises:
        ValueError: if any argument is not strictly positive.
    """
    if pressure_kpa <= 0:
        raise ValueError(f"pressure_kpa must be > 0, got {pressure_kpa}.")
    if temperature_k <= 0:
        raise ValueError(f"temperature_k must be > 0, got {temperature_k}.")
    if gas_constant <= 0:
        raise ValueError(f"gas_constant must be > 0, got {gas_constant}.")

    pressure_pa = pressure_kpa * 1000.0
    return pressure_pa / (gas_constant * temperature_k)


def calculate_speed_of_sound(
    gamma: float,
    gas_constant: float,
    temperature_k: float,
) -> float:
    """Compute the speed of sound for a calorically perfect gas.

    Args:
        gamma: specific heat ratio. Must be > 1.
        gas_constant: specific gas constant R [J/(kg·K)]. Must be > 0.
        temperature_k: static temperature [K]. Must be > 0.

    Returns:
        Speed of sound [m/s].

    Raises:
        ValueError: if any argument violates its constraint.
    """
    if gamma <= 1:
        raise ValueError(f"gamma must be > 1, got {gamma}.")
    if gas_constant <= 0:
        raise ValueError(f"gas_constant must be > 0, got {gas_constant}.")
    if temperature_k <= 0:
        raise ValueError(f"temperature_k must be > 0, got {temperature_k}.")

    return math.sqrt(gamma * gas_constant * temperature_k)


def calculate_cp_air(temperature_k: float) -> float:
    """Estimate Cp of air using a linear approximation around 300 K.

    Args:
        temperature_k: static temperature [K]. Must be > 0.

    Returns:
        Specific heat at constant pressure Cp [J/(kg·K)].

    Raises:
        ValueError: if temperature_k <= 0.
    """
    if temperature_k <= 0:
        raise ValueError(f"temperature_k must be > 0, got {temperature_k}.")
    return 1005.0 + 0.1 * (temperature_k - 300.0)


def calculate_gamma(cp: float, gas_constant: float) -> float:
    """Compute the specific heat ratio gamma from Cp and R.

    Uses the relation gamma = Cp / Cv = Cp / (Cp - R).

    Args:
        cp: specific heat at constant pressure [J/(kg·K)]. Must be > gas_constant.
        gas_constant: specific gas constant R [J/(kg·K)]. Must be > 0.

    Returns:
        Specific heat ratio gamma (dimensionless).

    Raises:
        ValueError: if gas_constant <= 0 or cp <= gas_constant.
    """
    if gas_constant <= 0:
        raise ValueError(f"gas_constant must be > 0, got {gas_constant}.")
    if cp <= gas_constant:
        raise ValueError(
            f"cp ({cp}) must be greater than gas_constant ({gas_constant})."
        )
    return cp / (cp - gas_constant)


def speed_of_sound(gamma: float, R: float, T: float) -> float:
    """Compute the speed of sound for a calorically perfect gas.

    Args:
        gamma: specific heat ratio.
        R: specific gas constant [J/(kg·K)].
        T: static temperature [K].

    Returns:
        Speed of sound [m/s].
    """
    pass
