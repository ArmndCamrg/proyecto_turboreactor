"""Thermodynamic calculations for turbofan nozzle flow."""

from dataclasses import dataclass
import numpy as np
import pandas as pd
from src.gas_properties import GasProperties, calculate_density, calculate_speed_of_sound


@dataclass
class NozzleInputs:
    """Inputs required to analyze a converging or converging-diverging nozzle."""
    T0: float          # stagnation temperature [K]
    P0: float          # stagnation pressure [Pa]
    P_amb: float       # ambient (back) pressure [Pa]
    A_throat: float    # throat cross-sectional area [m²]
    A_exit: float      # exit cross-sectional area [m²]
    gas: GasProperties


@dataclass
class NozzleResults:
    """Computed results at the nozzle exit plane."""
    Mach_exit: float        # exit Mach number
    T_exit: float           # static temperature at exit [K]
    P_exit: float           # static pressure at exit [Pa]
    V_exit: float           # exit velocity [m/s]
    thrust: float           # gross thrust [N]
    mass_flow: float        # mass flow rate [kg/s]
    is_choked: bool         # whether throat is choked
    nozzle_type: str        # "converging" or "converging-diverging"


def isentropic_temperature_ratio(gamma: float, Mach: float) -> float:
    """Compute stagnation-to-static temperature ratio T0/T for isentropic flow.

    Args:
        gamma: specific heat ratio.
        Mach: local Mach number.

    Returns:
        T0/T ratio.
    """
    pass


def isentropic_pressure_ratio(gamma: float, Mach: float) -> float:
    """Compute stagnation-to-static pressure ratio P0/P for isentropic flow.

    Args:
        gamma: specific heat ratio.
        Mach: local Mach number.

    Returns:
        P0/P ratio.
    """
    pass


def critical_pressure_ratio(gamma: float) -> float:
    """Compute the critical pressure ratio P0/P* that chokes the throat.

    Args:
        gamma: specific heat ratio.

    Returns:
        Critical pressure ratio (P0/P*).
    """
    pass


def mach_from_area_ratio(area_ratio: float, gamma: float, supersonic: bool = False) -> float:
    """Solve for Mach number given area ratio A/A* using Newton-Raphson iteration.

    Args:
        area_ratio: local area divided by throat area (A/A*).
        gamma: specific heat ratio.
        supersonic: if True, return the supersonic solution branch.

    Returns:
        Mach number.
    """
    pass


def compute_mass_flow(P0: float, T0: float, A_throat: float, gas: GasProperties) -> float:
    """Compute choked mass flow rate through the throat.

    Args:
        P0: stagnation pressure [Pa].
        T0: stagnation temperature [K].
        A_throat: throat area [m²].
        gas: GasProperties instance.

    Returns:
        Mass flow rate [kg/s].
    """
    pass


def generate_pressure_range(
    inlet_pressure_kpa: float,
    outlet_pressure_kpa: float,
    num_points: int,
) -> np.ndarray:
    """Return evenly spaced pressures from inlet to outlet.

    Args:
        inlet_pressure_kpa: upstream stagnation pressure [kPa]. Must be greater than outlet.
        outlet_pressure_kpa: downstream back pressure [kPa].
        num_points: number of points in the array. Must be greater than 1.

    Returns:
        1-D numpy array of pressures in descending order [kPa].

    Raises:
        ValueError: if inlet_pressure_kpa <= outlet_pressure_kpa or num_points <= 1.
    """
    if inlet_pressure_kpa <= outlet_pressure_kpa:
        raise ValueError(
            f"inlet_pressure_kpa ({inlet_pressure_kpa}) must be greater than "
            f"outlet_pressure_kpa ({outlet_pressure_kpa})."
        )
    if num_points <= 1:
        raise ValueError(f"num_points must be greater than 1, got {num_points}.")
    return np.linspace(inlet_pressure_kpa, outlet_pressure_kpa, num_points)


def calculate_velocity_from_mach(mach_number: float, speed_of_sound: float) -> float:
    """Compute flow velocity from Mach number and local speed of sound.

    Args:
        mach_number: local Mach number. Must be >= 0.
        speed_of_sound: local speed of sound [m/s]. Must be > 0.

    Returns:
        Flow velocity [m/s].

    Raises:
        ValueError: if mach_number < 0 or speed_of_sound <= 0.
    """
    if mach_number < 0:
        raise ValueError(f"mach_number must be >= 0, got {mach_number}.")
    if speed_of_sound <= 0:
        raise ValueError(f"speed_of_sound must be > 0, got {speed_of_sound}.")
    return mach_number * speed_of_sound


def calculate_mach_number(velocity: float, speed_of_sound: float) -> float:
    """Compute Mach number from flow velocity and local speed of sound.

    Args:
        velocity: flow velocity [m/s]. Must be >= 0.
        speed_of_sound: local speed of sound [m/s]. Must be > 0.

    Returns:
        Mach number (dimensionless).

    Raises:
        ValueError: if velocity < 0 or speed_of_sound <= 0.
    """
    if velocity < 0:
        raise ValueError(f"velocity must be >= 0, got {velocity}.")
    if speed_of_sound <= 0:
        raise ValueError(f"speed_of_sound must be > 0, got {speed_of_sound}.")
    return velocity / speed_of_sound


def calculate_flow_area(
    mass_flow_rate: float,
    density: float,
    velocity: float,
) -> float:
    """Compute the cross-sectional flow area from the continuity equation.

    Args:
        mass_flow_rate: mass flow rate [kg/s]. Must be > 0.
        density: gas density [kg/m³]. Must be > 0.
        velocity: flow velocity [m/s]. Must be > 0.

    Returns:
        Cross-sectional area [m²].

    Raises:
        ValueError: if any argument is not strictly positive.
    """
    if mass_flow_rate <= 0:
        raise ValueError(f"mass_flow_rate must be > 0, got {mass_flow_rate}.")
    if density <= 0:
        raise ValueError(f"density must be > 0, got {density}.")
    if velocity <= 0:
        raise ValueError(f"velocity must be > 0, got {velocity}.")
    return mass_flow_rate / (density * velocity)


def build_results_table(
    inlet_pressure_kpa: float,
    outlet_pressure_kpa: float,
    num_points: int,
    temperature_k: float,
    gas_constant: float,
    gamma: float,
    mach_number: float,
    mass_flow_rate: float,
) -> pd.DataFrame:
    """Build a results table with thermodynamic properties across a pressure range.

    Uses a constant temperature, Mach number, and mass flow rate at each pressure
    point to compute density, velocity, and flow area.

    Args:
        inlet_pressure_kpa: upstream pressure [kPa]. Must be > outlet.
        outlet_pressure_kpa: downstream pressure [kPa].
        num_points: number of evenly spaced pressure points. Must be > 1.
        temperature_k: static temperature [K]. Must be > 0.
        gas_constant: specific gas constant R [J/(kg·K)]. Must be > 0.
        gamma: specific heat ratio. Must be > 1.
        mach_number: local Mach number. Must be >= 0.
        mass_flow_rate: mass flow rate [kg/s]. Must be > 0.

    Returns:
        DataFrame with columns: pressure_kpa, temperature_k, speed_of_sound_m_s,
        velocity_m_s, mach_number, density_kg_m3, flow_area_m2.
    """
    pressures = generate_pressure_range(inlet_pressure_kpa, outlet_pressure_kpa, num_points)
    a = calculate_speed_of_sound(gamma, gas_constant, temperature_k)
    velocity = calculate_velocity_from_mach(mach_number, a)

    densities = np.array([
        calculate_density(p, temperature_k, gas_constant) for p in pressures
    ])
    flow_areas = np.array([
        calculate_flow_area(mass_flow_rate, rho, velocity) for rho in densities
    ])
    mach_numbers = np.array([
        calculate_mach_number(velocity, a) for _ in pressures
    ])

    return pd.DataFrame({
        "pressure_kpa": pressures,
        "temperature_k": temperature_k,
        "speed_of_sound_m_s": a,
        "velocity_m_s": velocity,
        "mach_number": mach_numbers,
        "density_kg_m3": densities,
        "flow_area_m2": flow_areas,
    })


def analyze_nozzle(inputs: NozzleInputs) -> NozzleResults:
    """Run a complete 1-D isentropic nozzle analysis.

    Determines whether the nozzle is choked, computes exit conditions,
    and calculates gross thrust.

    Args:
        inputs: NozzleInputs with geometry and flow conditions.

    Returns:
        NozzleResults with all computed quantities.
    """
    pass
