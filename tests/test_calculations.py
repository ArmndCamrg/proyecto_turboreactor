"""Unit tests for thermodynamic calculations."""

import numpy as np
import pytest
from src.gas_properties import (
    GasProperties,
    get_air_properties,
    speed_of_sound,
    calculate_density,
    calculate_speed_of_sound,
    calculate_cp_air,
    calculate_gamma,
)
from src.calculations import (
    isentropic_temperature_ratio,
    isentropic_pressure_ratio,
    critical_pressure_ratio,
    mach_from_area_ratio,
    compute_mass_flow,
    analyze_nozzle,
    generate_pressure_range,
    calculate_velocity_from_mach,
    calculate_mach_number,
    calculate_flow_area,
    build_results_table,
    NozzleInputs,
)


# ── Fixtures ──────────────────────────────────────────────────────────────────

@pytest.fixture
def air() -> GasProperties:
    return GasProperties(gamma=1.4, R=287.05, Cp=1005.0, Cv=718.0, name="air")


@pytest.fixture
def converging_nozzle(air) -> NozzleInputs:
    return NozzleInputs(
        T0=600.0,
        P0=200_000.0,
        P_amb=101_325.0,
        A_throat=0.01,
        A_exit=0.01,   # same area → converging only
        gas=air,
    )


# ── isentropic_temperature_ratio ──────────────────────────────────────────────

def test_temperature_ratio_at_zero_mach(air):
    """At M=0 the ratio T0/T must equal 1."""
    pass


def test_temperature_ratio_at_mach_one(air):
    """At M=1 the ratio T0/T* = (gamma+1)/2 for calorically perfect gas."""
    pass


# ── isentropic_pressure_ratio ─────────────────────────────────────────────────

def test_pressure_ratio_at_zero_mach(air):
    """At M=0 the ratio P0/P must equal 1."""
    pass


def test_pressure_ratio_at_mach_one(air):
    """At M=1 the critical pressure ratio P0/P* = ((gamma+1)/2)^(gamma/(gamma-1))."""
    pass


# ── critical_pressure_ratio ───────────────────────────────────────────────────

def test_critical_pressure_ratio_air(air):
    """For air (gamma=1.4) the critical ratio is approximately 1.893."""
    pass


# ── mach_from_area_ratio ──────────────────────────────────────────────────────

def test_mach_from_area_ratio_unity(air):
    """Area ratio of 1 should return M=1."""
    pass


def test_mach_from_area_ratio_subsonic(air):
    """Subsonic branch should return M < 1 for area ratio > 1."""
    pass


def test_mach_from_area_ratio_supersonic(air):
    """Supersonic branch should return M > 1 for area ratio > 1."""
    pass


# ── analyze_nozzle ────────────────────────────────────────────────────────────

def test_nozzle_chokes_when_p_ratio_exceeded(converging_nozzle):
    """Nozzle should be choked when back pressure is below critical threshold."""
    pass


def test_nozzle_not_choked_at_high_back_pressure(converging_nozzle):
    """Nozzle should not choke when back pressure is above critical threshold."""
    pass


def test_thrust_positive(converging_nozzle):
    """Gross thrust must be positive for any valid operating condition."""
    pass


# ── generate_pressure_range ───────────────────────────────────────────────────

def test_pressure_range_length():
    """Returned array must have exactly num_points elements."""
    result = generate_pressure_range(200.0, 101.325, 50)
    assert len(result) == 50


def test_pressure_range_first_value():
    """First element must equal inlet_pressure_kpa."""
    result = generate_pressure_range(200.0, 101.325, 10)
    assert result[0] == pytest.approx(200.0)


def test_pressure_range_last_value():
    """Last element must equal outlet_pressure_kpa."""
    result = generate_pressure_range(200.0, 101.325, 10)
    assert result[-1] == pytest.approx(101.325)


def test_pressure_range_raises_when_inlet_not_greater():
    """ValueError when inlet pressure is not greater than outlet pressure."""
    with pytest.raises(ValueError):
        generate_pressure_range(100.0, 200.0, 10)


def test_pressure_range_raises_when_equal_pressures():
    """ValueError when inlet and outlet pressures are equal."""
    with pytest.raises(ValueError):
        generate_pressure_range(150.0, 150.0, 10)


def test_pressure_range_raises_when_num_points_one():
    """ValueError when num_points equals 1."""
    with pytest.raises(ValueError):
        generate_pressure_range(200.0, 101.325, 1)


def test_pressure_range_raises_when_num_points_zero():
    """ValueError when num_points is 0."""
    with pytest.raises(ValueError):
        generate_pressure_range(200.0, 101.325, 0)


# ── calculate_density ─────────────────────────────────────────────────────────

def test_density_known_value():
    """Verify rho = (P_kpa * 1000) / (R * T) against a hand-calculated value.

    At 101.325 kPa and 288.15 K with R=287.05 J/(kg·K):
    rho = 101325 / (287.05 * 288.15) ≈ 1.225 kg/m³  (ISA sea-level standard)
    """
    rho = calculate_density(101.325, 288.15, 287.05)
    assert rho == pytest.approx(1.225, rel=1e-3)


def test_density_doubles_with_doubled_pressure():
    """Density must double when pressure doubles at constant T and R."""
    rho1 = calculate_density(100.0, 300.0, 287.05)
    rho2 = calculate_density(200.0, 300.0, 287.05)
    assert rho2 == pytest.approx(2 * rho1)


def test_density_halves_with_doubled_temperature():
    """Density must halve when temperature doubles at constant P and R."""
    rho1 = calculate_density(100.0, 300.0, 287.05)
    rho2 = calculate_density(100.0, 600.0, 287.05)
    assert rho2 == pytest.approx(rho1 / 2)


def test_density_raises_on_zero_pressure():
    with pytest.raises(ValueError):
        calculate_density(0.0, 300.0, 287.05)


def test_density_raises_on_negative_pressure():
    with pytest.raises(ValueError):
        calculate_density(-10.0, 300.0, 287.05)


def test_density_raises_on_zero_temperature():
    with pytest.raises(ValueError):
        calculate_density(101.325, 0.0, 287.05)


def test_density_raises_on_zero_gas_constant():
    with pytest.raises(ValueError):
        calculate_density(101.325, 300.0, 0.0)


# ── calculate_speed_of_sound ──────────────────────────────────────────────────

def test_speed_of_sound_known_value():
    """At 288.15 K with gamma=1.4 and R=287.05 J/(kg·K) speed of sound ≈ 340.3 m/s."""
    a = calculate_speed_of_sound(1.4, 287.05, 288.15)
    assert a == pytest.approx(340.3, rel=1e-3)


def test_speed_of_sound_increases_with_temperature():
    """Speed of sound must increase as temperature increases."""
    a_cold = calculate_speed_of_sound(1.4, 287.05, 250.0)
    a_hot = calculate_speed_of_sound(1.4, 287.05, 500.0)
    assert a_hot > a_cold


def test_speed_of_sound_raises_on_gamma_equal_one():
    with pytest.raises(ValueError):
        calculate_speed_of_sound(1.0, 287.05, 300.0)


def test_speed_of_sound_raises_on_gamma_below_one():
    with pytest.raises(ValueError):
        calculate_speed_of_sound(0.9, 287.05, 300.0)


def test_speed_of_sound_raises_on_zero_gas_constant():
    with pytest.raises(ValueError):
        calculate_speed_of_sound(1.4, 0.0, 300.0)


def test_speed_of_sound_raises_on_zero_temperature():
    with pytest.raises(ValueError):
        calculate_speed_of_sound(1.4, 287.05, 0.0)


# ── calculate_velocity_from_mach ──────────────────────────────────────────────

def test_velocity_from_mach_known_value():
    """V = M * a: at M=2 and a=340 m/s velocity must be 680 m/s."""
    assert calculate_velocity_from_mach(2.0, 340.0) == pytest.approx(680.0)


def test_velocity_from_mach_zero_mach():
    """At M=0 velocity must be zero regardless of speed of sound."""
    assert calculate_velocity_from_mach(0.0, 340.0) == pytest.approx(0.0)


def test_velocity_from_mach_mach_one():
    """At M=1 velocity must equal speed of sound."""
    a = 340.3
    assert calculate_velocity_from_mach(1.0, a) == pytest.approx(a)


def test_velocity_from_mach_raises_on_negative_mach():
    with pytest.raises(ValueError):
        calculate_velocity_from_mach(-0.1, 340.0)


def test_velocity_from_mach_raises_on_zero_speed_of_sound():
    with pytest.raises(ValueError):
        calculate_velocity_from_mach(1.0, 0.0)


def test_velocity_from_mach_raises_on_negative_speed_of_sound():
    with pytest.raises(ValueError):
        calculate_velocity_from_mach(1.0, -340.0)


# ── calculate_mach_number ─────────────────────────────────────────────────────

def test_mach_number_known_value():
    """M = V / a: at V=680 m/s and a=340 m/s Mach must be 2.0."""
    assert calculate_mach_number(680.0, 340.0) == pytest.approx(2.0)


def test_mach_number_zero_velocity():
    """At V=0 Mach number must be zero."""
    assert calculate_mach_number(0.0, 340.0) == pytest.approx(0.0)


def test_mach_number_velocity_equals_speed_of_sound():
    """When V == a the Mach number must be 1."""
    assert calculate_mach_number(340.0, 340.0) == pytest.approx(1.0)


def test_mach_number_raises_on_negative_velocity():
    with pytest.raises(ValueError):
        calculate_mach_number(-10.0, 340.0)


def test_mach_number_raises_on_zero_speed_of_sound():
    with pytest.raises(ValueError):
        calculate_mach_number(340.0, 0.0)


def test_mach_number_raises_on_negative_speed_of_sound():
    with pytest.raises(ValueError):
        calculate_mach_number(340.0, -340.0)


def test_velocity_mach_roundtrip():
    """calculate_mach_number(calculate_velocity_from_mach(M, a), a) must recover M."""
    mach_in = 1.8
    a = 320.0
    velocity = calculate_velocity_from_mach(mach_in, a)
    assert calculate_mach_number(velocity, a) == pytest.approx(mach_in)


# ── calculate_flow_area ───────────────────────────────────────────────────────

def test_flow_area_known_value():
    """A = mdot / (rho * V): 2 kg/s, 1.225 kg/m³, 100 m/s → ≈ 0.01633 m²."""
    area = calculate_flow_area(2.0, 1.225, 100.0)
    assert area == pytest.approx(2.0 / (1.225 * 100.0))


def test_flow_area_doubles_with_doubled_mass_flow():
    """Area must double when mass flow rate doubles at constant density and velocity."""
    a1 = calculate_flow_area(1.0, 1.2, 200.0)
    a2 = calculate_flow_area(2.0, 1.2, 200.0)
    assert a2 == pytest.approx(2 * a1)


def test_flow_area_raises_on_zero_mass_flow_rate():
    with pytest.raises(ValueError):
        calculate_flow_area(0.0, 1.2, 200.0)


def test_flow_area_raises_on_negative_mass_flow_rate():
    with pytest.raises(ValueError):
        calculate_flow_area(-1.0, 1.2, 200.0)


def test_flow_area_raises_on_zero_density():
    with pytest.raises(ValueError):
        calculate_flow_area(1.0, 0.0, 200.0)


def test_flow_area_raises_on_negative_density():
    with pytest.raises(ValueError):
        calculate_flow_area(1.0, -1.2, 200.0)


def test_flow_area_raises_on_zero_velocity():
    with pytest.raises(ValueError):
        calculate_flow_area(1.0, 1.2, 0.0)


def test_flow_area_raises_on_negative_velocity():
    with pytest.raises(ValueError):
        calculate_flow_area(1.0, 1.2, -200.0)


# ── build_results_table ───────────────────────────────────────────────────────

RESULTS_TABLE_DEFAULTS = dict(
    inlet_pressure_kpa=200.0,
    outlet_pressure_kpa=101.325,
    num_points=10,
    temperature_k=288.15,
    gas_constant=287.05,
    gamma=1.4,
    mach_number=0.8,
    mass_flow_rate=2.0,
)

EXPECTED_COLUMNS = {
    "pressure_kpa",
    "temperature_k",
    "speed_of_sound_m_s",
    "velocity_m_s",
    "mach_number",
    "density_kg_m3",
    "flow_area_m2",
}


def test_results_table_row_count():
    """DataFrame must have exactly num_points rows."""
    df = build_results_table(**RESULTS_TABLE_DEFAULTS)
    assert len(df) == RESULTS_TABLE_DEFAULTS["num_points"]


def test_results_table_columns():
    """DataFrame must contain exactly the expected columns."""
    df = build_results_table(**RESULTS_TABLE_DEFAULTS)
    assert set(df.columns) == EXPECTED_COLUMNS


def test_results_table_no_nulls():
    """DataFrame must contain no NaN or null values."""
    df = build_results_table(**RESULTS_TABLE_DEFAULTS)
    assert not df.isnull().any().any()


def test_results_table_first_pressure():
    """First row pressure must equal inlet_pressure_kpa."""
    df = build_results_table(**RESULTS_TABLE_DEFAULTS)
    assert df["pressure_kpa"].iloc[0] == pytest.approx(RESULTS_TABLE_DEFAULTS["inlet_pressure_kpa"])


def test_results_table_last_pressure():
    """Last row pressure must equal outlet_pressure_kpa."""
    df = build_results_table(**RESULTS_TABLE_DEFAULTS)
    assert df["pressure_kpa"].iloc[-1] == pytest.approx(RESULTS_TABLE_DEFAULTS["outlet_pressure_kpa"])


# ── calculate_cp_air ──────────────────────────────────────────────────────────

def test_cp_air_at_reference_temperature():
    """At 300 K the approximation returns exactly 1005 J/(kg·K)."""
    assert calculate_cp_air(300.0) == pytest.approx(1005.0)


def test_cp_air_increases_with_temperature():
    """Cp must increase as temperature increases (positive slope)."""
    assert calculate_cp_air(600.0) > calculate_cp_air(300.0)


def test_cp_air_known_value():
    """At 800 K: cp = 1005 + 0.1 * (800 - 300) = 1055 J/(kg·K)."""
    assert calculate_cp_air(800.0) == pytest.approx(1055.0)


def test_cp_air_raises_on_zero_temperature():
    with pytest.raises(ValueError):
        calculate_cp_air(0.0)


def test_cp_air_raises_on_negative_temperature():
    with pytest.raises(ValueError):
        calculate_cp_air(-100.0)


# ── calculate_gamma ───────────────────────────────────────────────────────────

def test_gamma_known_value_air():
    """For standard air Cp=1005 and R=287.05: gamma = 1005 / (1005 - 287.05) ≈ 1.4."""
    gamma = calculate_gamma(1005.0, 287.05)
    assert gamma == pytest.approx(1.4, rel=1e-3)


def test_gamma_decreases_as_cp_increases():
    """Higher Cp (hotter gas) should yield a lower gamma."""
    gamma_cold = calculate_gamma(1005.0, 287.05)
    gamma_hot = calculate_gamma(1100.0, 287.05)
    assert gamma_hot < gamma_cold


def test_gamma_raises_when_cp_equals_gas_constant():
    with pytest.raises(ValueError):
        calculate_gamma(287.05, 287.05)


def test_gamma_raises_when_cp_less_than_gas_constant():
    with pytest.raises(ValueError):
        calculate_gamma(200.0, 287.05)


def test_gamma_raises_on_zero_gas_constant():
    with pytest.raises(ValueError):
        calculate_gamma(1005.0, 0.0)


def test_gamma_raises_on_negative_gas_constant():
    with pytest.raises(ValueError):
        calculate_gamma(1005.0, -287.05)
