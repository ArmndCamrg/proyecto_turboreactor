"""Thermodynamic calculations for turbofan nozzle flow."""

from dataclasses import dataclass
import math
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
    mass_flow_rate: float,
    **_kwargs,
) -> pd.DataFrame:
    """Build a results table with isentropic thermodynamic properties across a pressure range.

    Treats inlet_pressure_kpa as stagnation pressure P0 and each point in the
    generated range as a local static pressure. Mach number and all derived
    quantities are computed per point from the pressure ratio.

    At the inlet point (static == total pressure) Mach=0, velocity=0 and
    flow_area_m2 is NaN because the cross-section is physically undefined.

    Args:
        inlet_pressure_kpa: stagnation pressure P0 [kPa]. Must be > outlet.
        outlet_pressure_kpa: exit static pressure [kPa].
        num_points: number of evenly spaced pressure points. Must be > 1.
        temperature_k: stagnation temperature T0 [K]. Must be > 0.
        gas_constant: specific gas constant R [J/(kg·K)]. Must be > 0.
        gamma: specific heat ratio. Must be > 1.
        mass_flow_rate: mass flow rate [kg/s]. Must be > 0.
        **_kwargs: absorbs legacy keyword arguments (e.g. mach_number) for
            backward compatibility.

    Returns:
        DataFrame with columns: pressure_kpa, static_temperature_k,
        speed_of_sound_m_s, velocity_m_s, mach_number, density_kg_m3,
        flow_area_m2.
    """
    pressures = generate_pressure_range(inlet_pressure_kpa, outlet_pressure_kpa, num_points)

    machs = np.array([
        calculate_mach_from_pressure_ratio(inlet_pressure_kpa, p, gamma)
        for p in pressures
    ])
    static_temps = np.array([
        calculate_static_temperature(temperature_k, gamma, m) for m in machs
    ])
    speeds_of_sound = np.array([
        calculate_speed_of_sound(gamma, gas_constant, t) for t in static_temps
    ])
    velocities = np.array([
        calculate_velocity_from_temperature(gamma, gas_constant, temperature_k, t)
        if t < temperature_k else 0.0
        for t in static_temps
    ])
    densities = np.array([
        calculate_density(p, t, gas_constant)
        for p, t in zip(pressures, static_temps)
    ])
    flow_areas = np.array([
        calculate_flow_area(mass_flow_rate, rho, v) if v > 0.0 else np.nan
        for rho, v in zip(densities, velocities)
    ])

    return pd.DataFrame({
        "pressure_kpa": pressures,
        "static_temperature_k": static_temps,
        "speed_of_sound_m_s": speeds_of_sound,
        "velocity_m_s": velocities,
        "mach_number": machs,
        "density_kg_m3": densities,
        "flow_area_m2": flow_areas,
    })


def calculate_static_temperature(
    total_temperature_k: float,
    gamma: float,
    mach_number: float,
) -> float:
    """Compute static temperature from stagnation temperature using isentropic relation.

    Args:
        total_temperature_k: stagnation (total) temperature T0 [K]. Must be > 0.
        gamma: specific heat ratio. Must be > 1.
        mach_number: local Mach number. Must be >= 0.

    Returns:
        Static temperature T [K].

    Raises:
        ValueError: if any argument violates its constraint.
    """
    if total_temperature_k <= 0:
        raise ValueError(f"total_temperature_k must be > 0, got {total_temperature_k}.")
    if gamma <= 1:
        raise ValueError(f"gamma must be > 1, got {gamma}.")
    if mach_number < 0:
        raise ValueError(f"mach_number must be >= 0, got {mach_number}.")
    return total_temperature_k / (1.0 + ((gamma - 1.0) / 2.0) * mach_number ** 2)


def calculate_static_pressure(
    total_pressure_kpa: float,
    gamma: float,
    mach_number: float,
) -> float:
    """Compute static pressure from stagnation pressure using isentropic relation.

    Args:
        total_pressure_kpa: stagnation (total) pressure P0 [kPa]. Must be > 0.
        gamma: specific heat ratio. Must be > 1.
        mach_number: local Mach number. Must be >= 0.

    Returns:
        Static pressure P [kPa].

    Raises:
        ValueError: if any argument violates its constraint.
    """
    if total_pressure_kpa <= 0:
        raise ValueError(f"total_pressure_kpa must be > 0, got {total_pressure_kpa}.")
    if gamma <= 1:
        raise ValueError(f"gamma must be > 1, got {gamma}.")
    if mach_number < 0:
        raise ValueError(f"mach_number must be >= 0, got {mach_number}.")
    exponent = gamma / (gamma - 1.0)
    return total_pressure_kpa / (1.0 + ((gamma - 1.0) / 2.0) * mach_number ** 2) ** exponent


def calculate_velocity_from_temperature(
    gamma: float,
    gas_constant: float,
    total_temperature_k: float,
    static_temperature_k: float,
) -> float:
    """Compute flow velocity from the isentropic enthalpy drop between total and static states.

    Args:
        gamma: specific heat ratio. Must be > 1.
        gas_constant: specific gas constant R [J/(kg·K)]. Must be > 0.
        total_temperature_k: stagnation temperature T0 [K]. Must be > static_temperature_k.
        static_temperature_k: static temperature T [K]. Must be > 0.

    Returns:
        Flow velocity [m/s].

    Raises:
        ValueError: if any argument violates its constraint.
    """
    if gamma <= 1:
        raise ValueError(f"gamma must be > 1, got {gamma}.")
    if gas_constant <= 0:
        raise ValueError(f"gas_constant must be > 0, got {gas_constant}.")
    if static_temperature_k <= 0:
        raise ValueError(f"static_temperature_k must be > 0, got {static_temperature_k}.")
    if total_temperature_k <= static_temperature_k:
        raise ValueError(
            f"total_temperature_k ({total_temperature_k}) must be greater than "
            f"static_temperature_k ({static_temperature_k})."
        )
    delta_t = total_temperature_k - static_temperature_k
    return math.sqrt(2.0 * gamma * gas_constant * delta_t / (gamma - 1.0))


def calculate_mach_from_pressure_ratio(
    total_pressure_kpa: float,
    static_pressure_kpa: float,
    gamma: float,
) -> float:
    """Compute Mach number from the isentropic total-to-static pressure ratio.

    Args:
        total_pressure_kpa: stagnation pressure P0 [kPa]. Must be > 0.
        static_pressure_kpa: static pressure P [kPa]. Must be > 0.
        gamma: specific heat ratio. Must be > 1.

    Returns:
        Mach number (dimensionless).

    Raises:
        ValueError: if any argument violates its constraint or P0 < P.
    """
    if total_pressure_kpa <= 0:
        raise ValueError(f"total_pressure_kpa must be > 0, got {total_pressure_kpa}.")
    if static_pressure_kpa <= 0:
        raise ValueError(f"static_pressure_kpa must be > 0, got {static_pressure_kpa}.")
    if total_pressure_kpa < static_pressure_kpa:
        raise ValueError(
            f"total_pressure_kpa ({total_pressure_kpa}) must be >= "
            f"static_pressure_kpa ({static_pressure_kpa})."
        )
    if gamma <= 1:
        raise ValueError(f"gamma must be > 1, got {gamma}.")
    pressure_ratio = total_pressure_kpa / static_pressure_kpa
    return math.sqrt(
        (2.0 / (gamma - 1.0)) * (pressure_ratio ** ((gamma - 1.0) / gamma) - 1.0)
    )


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
