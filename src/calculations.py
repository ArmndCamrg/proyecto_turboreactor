"""Cálculos termodinámicos para el flujo en toberas de turbofán.

Supuestos físicos generales del módulo
---------------------------------------
- Flujo isentrópico (adiabático y sin fricción) en todo el dominio.
- Flujo 1-D: las propiedades del gas son uniformes en cada sección transversal.
- Gas caloricamente perfecto: γ, Cp y R constantes a lo largo del análisis.
- La presión de remanso (total) P₀ es constante aguas arriba de la tobera.
- El gasto másico ṁ se conserva a lo largo de la tobera.
"""

from dataclasses import dataclass
import math
import numpy as np
import pandas as pd
from src.gas_properties import GasProperties, calculate_density, calculate_speed_of_sound


@dataclass
class NozzleInputs:
    """Parámetros de entrada para el análisis de una tobera convergente o convergente-divergente.

    Atributos
    ---------
    T0 : float
        Temperatura de remanso (total) aguas arriba [K].
    P0 : float
        Presión de remanso (total) aguas arriba [Pa].
    P_amb : float
        Presión ambiente o de descarga (contrapresión) [Pa].
    A_throat : float
        Área de la garganta (sección mínima) [m²].
    A_exit : float
        Área de la sección de salida [m²].
    gas : GasProperties
        Propiedades termodinámicas del gas de trabajo.
    """
    T0: float          # temperatura de remanso [K]
    P0: float          # presión de remanso [Pa]
    P_amb: float       # presión ambiente / contrapresión [Pa]
    A_throat: float    # área de la garganta [m²]
    A_exit: float      # área de la sección de salida [m²]
    gas: GasProperties


@dataclass
class NozzleResults:
    """Resultados calculados en el plano de salida de la tobera.

    Atributos
    ---------
    Mach_exit : float
        Número de Mach en la sección de salida (adimensional).
    T_exit : float
        Temperatura estática en la salida [K].
    P_exit : float
        Presión estática en la salida [Pa].
    V_exit : float
        Velocidad del gas en la salida [m/s].
    thrust : float
        Empuje bruto de la tobera [N].
    mass_flow : float
        Gasto másico [kg/s].
    is_choked : bool
        True si la garganta está ahogada (flujo sónico en garganta).
    nozzle_type : str
        Tipo de tobera: "converging" o "converging-diverging".
    """
    Mach_exit: float        # Mach en la salida
    T_exit: float           # temperatura estática en salida [K]
    P_exit: float           # presión estática en salida [Pa]
    V_exit: float           # velocidad en salida [m/s]
    thrust: float           # empuje bruto [N]
    mass_flow: float        # gasto másico [kg/s]
    is_choked: bool         # True si el flujo está ahogado en la garganta
    nozzle_type: str        # "converging" o "converging-diverging"


def isentropic_temperature_ratio(gamma: float, Mach: float) -> float:
    """Calcula la razón de temperatura de remanso a temperatura estática T₀/T.

    Supuestos
    ---------
    - Flujo isentrópico de un gas caloricamente perfecto.

    Fórmula
    -------
    T₀/T = 1 + ((γ-1)/2) × M²

    Esta relación se obtiene de la definición de entalpía de remanso y la
    ecuación de energía para flujo adiabático sin trabajo de eje.

    Parámetros
    ----------
    gamma : float
        Razón de calores específicos γ (adimensional).
    Mach : float
        Número de Mach local M (adimensional).

    Retorna
    -------
    float
        Razón T₀/T (adimensional).
    """
    pass


def isentropic_pressure_ratio(gamma: float, Mach: float) -> float:
    """Calcula la razón de presión de remanso a presión estática P₀/P.

    Supuestos
    ---------
    - Flujo isentrópico de un gas caloricamente perfecto.

    Fórmula
    -------
    P₀/P = (T₀/T)^(γ/(γ-1)) = [1 + ((γ-1)/2) × M²]^(γ/(γ-1))

    Deriva de combinar la razón de temperatura isentrópica con la relación
    politrópica P ∝ ρ^γ bajo condiciones isentrópicas.

    Parámetros
    ----------
    gamma : float
        Razón de calores específicos γ (adimensional).
    Mach : float
        Número de Mach local M (adimensional).

    Retorna
    -------
    float
        Razón P₀/P (adimensional).
    """
    pass


def critical_pressure_ratio(gamma: float) -> float:
    """Calcula la razón crítica de presión P₀/P* que ahoga la garganta.

    Supuestos
    ---------
    - La condición crítica ocurre cuando M = 1 en la garganta.
    - Flujo isentrópico de un gas caloricamente perfecto.

    Fórmula
    -------
    P₀/P* = [(γ+1)/2]^(γ/(γ-1))

    Para aire (γ = 1.4): P₀/P* ≈ 1.893.
    Si P₀/P_salida ≥ P₀/P* el flujo en la garganta es sónico (ahogado).

    Parámetros
    ----------
    gamma : float
        Razón de calores específicos γ (adimensional).

    Retorna
    -------
    float
        Razón crítica de presión P₀/P* (adimensional).
    """
    pass


def mach_from_area_ratio(area_ratio: float, gamma: float, supersonic: bool = False) -> float:
    """Calcula el número de Mach dada la razón de área A/A* mediante iteración Newton-Raphson.

    Supuestos
    ---------
    - Flujo isentrópico 1-D en una tobera de sección variable.
    - A* es el área de la garganta donde M = 1.

    Fórmula implícita (ecuación de área-Mach)
    ------------------------------------------
    A/A* = (1/M) × [(2/(γ+1)) × (1 + (γ-1)/2 × M²)]^((γ+1)/(2(γ-1)))

    Esta ecuación tiene dos soluciones para A/A* > 1: una subsónica (M < 1)
    y una supersónica (M > 1). El parámetro `supersonic` selecciona la rama.

    Parámetros
    ----------
    area_ratio : float
        Razón de área local respecto a la garganta A/A* (adimensional). Debe ser ≥ 1.
    gamma : float
        Razón de calores específicos γ (adimensional).
    supersonic : bool
        Si True, devuelve la solución de la rama supersónica. Por defecto False.

    Retorna
    -------
    float
        Número de Mach M (adimensional).
    """
    pass


def compute_mass_flow(P0: float, T0: float, A_throat: float, gas: GasProperties) -> float:
    """Calcula el gasto másico para una garganta ahogada (M = 1).

    Supuestos
    ---------
    - La garganta opera en condición sónica (flujo ahogado).
    - Flujo isentrópico de un gas caloricamente perfecto.

    Fórmula
    -------
    ṁ = A* × P₀ × √(γ/(R T₀)) × [2/(γ+1)]^((γ+1)/(2(γ-1)))

    Esta expresión combina la ecuación de continuidad con las relaciones
    isentrópicas evaluadas en la condición crítica (M = 1).

    Parámetros
    ----------
    P0 : float
        Presión de remanso [Pa].
    T0 : float
        Temperatura de remanso [K].
    A_throat : float
        Área de la garganta A* [m²].
    gas : GasProperties
        Propiedades termodinámicas del gas.

    Retorna
    -------
    float
        Gasto másico ṁ [kg/s].
    """
    pass


def generate_pressure_range(
    inlet_pressure_kpa: float,
    outlet_pressure_kpa: float,
    num_points: int,
) -> np.ndarray:
    """Genera un arreglo de presiones uniformemente espaciadas de entrada a salida.

    Produce un barrido de presiones estáticas descendentes que representa la
    expansión del gas a lo largo de la tobera, desde la condición de remanso
    (entrada) hasta la presión de descarga (salida).

    Parámetros
    ----------
    inlet_pressure_kpa : float
        Presión de remanso en la entrada P₀ [kPa]. Debe ser > outlet.
    outlet_pressure_kpa : float
        Presión estática en la salida (contrapresión) [kPa].
    num_points : int
        Número de puntos en el arreglo. Debe ser > 1.

    Retorna
    -------
    np.ndarray
        Arreglo 1-D de presiones en orden descendente [kPa].

    Excepciones
    -----------
    ValueError
        Si inlet_pressure_kpa <= outlet_pressure_kpa o num_points <= 1.
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
    """Calcula la velocidad del flujo a partir del número de Mach y la velocidad del sonido.

    Supuestos
    ---------
    - La velocidad del sonido se evalúa a la temperatura estática local.

    Fórmula
    -------
    V = M × a

    Donde M es el número de Mach y a la velocidad del sonido local.

    Parámetros
    ----------
    mach_number : float
        Número de Mach local M (adimensional). Debe ser ≥ 0.
    speed_of_sound : float
        Velocidad del sonido local a [m/s]. Debe ser > 0.

    Retorna
    -------
    float
        Velocidad del flujo V [m/s].

    Excepciones
    -----------
    ValueError
        Si mach_number < 0 o speed_of_sound <= 0.
    """
    if mach_number < 0:
        raise ValueError(f"mach_number must be >= 0, got {mach_number}.")
    if speed_of_sound <= 0:
        raise ValueError(f"speed_of_sound must be > 0, got {speed_of_sound}.")
    # V = M × a
    return mach_number * speed_of_sound


def calculate_mach_number(velocity: float, speed_of_sound: float) -> float:
    """Calcula el número de Mach a partir de la velocidad del flujo y la velocidad del sonido.

    Supuestos
    ---------
    - La velocidad del sonido se evalúa a la temperatura estática local.

    Fórmula
    -------
    M = V / a

    Parámetros
    ----------
    velocity : float
        Velocidad del flujo V [m/s]. Debe ser ≥ 0.
    speed_of_sound : float
        Velocidad del sonido local a [m/s]. Debe ser > 0.

    Retorna
    -------
    float
        Número de Mach M (adimensional).

    Excepciones
    -----------
    ValueError
        Si velocity < 0 o speed_of_sound <= 0.
    """
    if velocity < 0:
        raise ValueError(f"velocity must be >= 0, got {velocity}.")
    if speed_of_sound <= 0:
        raise ValueError(f"speed_of_sound must be > 0, got {speed_of_sound}.")
    # M = V / a
    return velocity / speed_of_sound


def calculate_flow_area(
    mass_flow_rate: float,
    density: float,
    velocity: float,
) -> float:
    """Calcula el área transversal del flujo a partir de la ecuación de continuidad.

    Supuestos
    ---------
    - Flujo 1-D estacionario: ṁ = ρ A V = constante.
    - Las propiedades son uniformes en cada sección transversal.

    Fórmula
    -------
    A = ṁ / (ρ × V)

    Derivada de la ecuación de continuidad en forma integral para flujo
    estacionario con sección variable.

    Parámetros
    ----------
    mass_flow_rate : float
        Gasto másico ṁ [kg/s]. Debe ser > 0.
    density : float
        Densidad del gas ρ [kg/m³]. Debe ser > 0.
    velocity : float
        Velocidad del flujo V [m/s]. Debe ser > 0.

    Retorna
    -------
    float
        Área de la sección transversal A [m²].

    Excepciones
    -----------
    ValueError
        Si algún argumento no es estrictamente positivo.
    """
    if mass_flow_rate <= 0:
        raise ValueError(f"mass_flow_rate must be > 0, got {mass_flow_rate}.")
    if density <= 0:
        raise ValueError(f"density must be > 0, got {density}.")
    if velocity <= 0:
        raise ValueError(f"velocity must be > 0, got {velocity}.")
    # A = ṁ / (ρ V)  —  ecuación de continuidad despejada para el área
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
    """Construye una tabla de propiedades termodinámicas isentrópicas a lo largo de la tobera.

    Modelo de cálculo
    -----------------
    La presión de entrada se trata como presión total P₀. Cada valor del rango
    de presiones generado se trata como presión estática local P. A partir de la
    razón P₀/P se deriva el número de Mach y, en cascada, todas las demás
    propiedades termodinámicas locales mediante relaciones isentrópicas.

    Secuencia de cálculo por punto
    --------------------------------
    1. M  = f(P₀/P, γ)          → `calculate_mach_from_pressure_ratio`
    2. T  = T₀ / (1+(γ-1)/2·M²) → `calculate_static_temperature`
    3. a  = √(γ R T)             → `calculate_speed_of_sound`
    4. V  = √(2γR(T₀-T)/(γ-1))  → `calculate_velocity_from_temperature`
    5. ρ  = P/(R T)              → `calculate_density`
    6. A  = ṁ/(ρ V)              → `calculate_flow_area`

    Nota sobre el punto de entrada (P = P₀)
    -----------------------------------------
    En el punto inicial P = P₀, la razón P₀/P = 1 implica M = 0 y V = 0.
    El área de flujo es físicamente indefinida (fluido en reposo) y se
    registra como NaN en la columna `flow_area_m2`.

    Supuestos
    ---------
    - Flujo isentrópico 1-D de un gas caloricamente perfecto.
    - T₀ y ṁ constantes a lo largo del dominio.
    - La temperatura disminuye monótonamente al expandirse el gas.

    Parámetros
    ----------
    inlet_pressure_kpa : float
        Presión de remanso P₀ [kPa]. Debe ser > outlet.
    outlet_pressure_kpa : float
        Presión estática de descarga [kPa].
    num_points : int
        Número de puntos de discretización. Debe ser > 1.
    temperature_k : float
        Temperatura de remanso T₀ [K]. Debe ser > 0.
    gas_constant : float
        Constante específica del gas R [J/(kg·K)]. Debe ser > 0.
    gamma : float
        Razón de calores específicos γ. Debe ser > 1.
    mass_flow_rate : float
        Gasto másico ṁ [kg/s]. Debe ser > 0.
    **_kwargs
        Absorbe argumentos de versiones anteriores (p. ej. `mach_number`)
        para mantener compatibilidad con código existente.

    Retorna
    -------
    pd.DataFrame
        Tabla con columnas: pressure_kpa, static_temperature_k,
        speed_of_sound_m_s, velocity_m_s, mach_number, density_kg_m3,
        flow_area_m2.
    """
    # Paso 0: barrido de presiones estáticas de P₀ hasta P_salida
    pressures = generate_pressure_range(inlet_pressure_kpa, outlet_pressure_kpa, num_points)

    # Paso 1: Mach local desde la razón P₀/P_estática isentrópica
    machs = np.array([
        calculate_mach_from_pressure_ratio(inlet_pressure_kpa, p, gamma)
        for p in pressures
    ])

    # Paso 2: temperatura estática local T = T₀ / (1 + (γ-1)/2 · M²)
    static_temps = np.array([
        calculate_static_temperature(temperature_k, gamma, m) for m in machs
    ])

    # Paso 3: velocidad del sonido local a = √(γ R T)
    speeds_of_sound = np.array([
        calculate_speed_of_sound(gamma, gas_constant, t) for t in static_temps
    ])

    # Paso 4: velocidad del flujo V = √(2γR(T₀-T)/(γ-1))
    #         En el punto inicial T_estática = T₀ → M=0, se asigna V=0 directamente
    velocities = np.array([
        calculate_velocity_from_temperature(gamma, gas_constant, temperature_k, t)
        if t < temperature_k else 0.0
        for t in static_temps
    ])

    # Paso 5: densidad local ρ = P/(R T) con P en Pa
    densities = np.array([
        calculate_density(p, t, gas_constant)
        for p, t in zip(pressures, static_temps)
    ])

    # Paso 6: área transversal A = ṁ/(ρ V); indefinida cuando V=0 (punto de remanso)
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
    """Calcula la temperatura estática a partir de la temperatura de remanso (relación isentrópica).

    Supuestos
    ---------
    - Flujo isentrópico (adiabático y sin irreversibilidades).
    - Gas caloricamente perfecto con γ constante.

    Fórmula
    -------
    T = T₀ / [1 + ((γ-1)/2) × M²]

    Se desprende de la ecuación de energía para flujo adiabático:
    h₀ = h + V²/2  →  Cp T₀ = Cp T + V²/2
    combinada con la definición de Mach M = V/a y a = √(γRT).

    Parámetros
    ----------
    total_temperature_k : float
        Temperatura de remanso T₀ [K]. Debe ser > 0.
    gamma : float
        Razón de calores específicos γ. Debe ser > 1.
    mach_number : float
        Número de Mach local M. Debe ser ≥ 0.

    Retorna
    -------
    float
        Temperatura estática T [K].

    Excepciones
    -----------
    ValueError
        Si algún argumento viola su restricción.
    """
    if total_temperature_k <= 0:
        raise ValueError(f"total_temperature_k must be > 0, got {total_temperature_k}.")
    if gamma <= 1:
        raise ValueError(f"gamma must be > 1, got {gamma}.")
    if mach_number < 0:
        raise ValueError(f"mach_number must be >= 0, got {mach_number}.")
    # T = T₀ / (1 + (γ-1)/2 · M²)
    return total_temperature_k / (1.0 + ((gamma - 1.0) / 2.0) * mach_number ** 2)


def calculate_static_pressure(
    total_pressure_kpa: float,
    gamma: float,
    mach_number: float,
) -> float:
    """Calcula la presión estática a partir de la presión de remanso (relación isentrópica).

    Supuestos
    ---------
    - Flujo isentrópico de un gas caloricamente perfecto.

    Fórmula
    -------
    P = P₀ / [1 + ((γ-1)/2) × M²]^(γ/(γ-1))

    El exponente γ/(γ-1) proviene de la relación politrópica isentrópica
    P ∝ T^(γ/(γ-1)), que se obtiene combinando la ley del gas ideal con
    la condición ds = 0.

    Parámetros
    ----------
    total_pressure_kpa : float
        Presión de remanso P₀ [kPa]. Debe ser > 0.
    gamma : float
        Razón de calores específicos γ. Debe ser > 1.
    mach_number : float
        Número de Mach local M. Debe ser ≥ 0.

    Retorna
    -------
    float
        Presión estática P [kPa].

    Excepciones
    -----------
    ValueError
        Si algún argumento viola su restricción.
    """
    if total_pressure_kpa <= 0:
        raise ValueError(f"total_pressure_kpa must be > 0, got {total_pressure_kpa}.")
    if gamma <= 1:
        raise ValueError(f"gamma must be > 1, got {gamma}.")
    if mach_number < 0:
        raise ValueError(f"mach_number must be >= 0, got {mach_number}.")
    # Exponente de la relación isentrópica presión-temperatura
    exponent = gamma / (gamma - 1.0)
    # P = P₀ / (1 + (γ-1)/2 · M²)^(γ/(γ-1))
    return total_pressure_kpa / (1.0 + ((gamma - 1.0) / 2.0) * mach_number ** 2) ** exponent


def calculate_velocity_from_temperature(
    gamma: float,
    gas_constant: float,
    total_temperature_k: float,
    static_temperature_k: float,
) -> float:
    """Calcula la velocidad del flujo a partir de la caída de entalpía entre estado total y estático.

    Supuestos
    ---------
    - Flujo adiabático sin trabajo de eje: h₀ = h + V²/2.
    - Gas caloricamente perfecto: Δh = Cp ΔT.
    - Cp se expresa en función de γ y R: Cp = γR/(γ-1).

    Fórmula
    -------
    V = √[2γR(T₀ - T) / (γ-1)]

    Derivación:
      h₀ - h = V²/2  →  Cp(T₀ - T) = V²/2
      Cp = γR/(γ-1)  →  V = √[2γR(T₀-T)/(γ-1)]

    Parámetros
    ----------
    gamma : float
        Razón de calores específicos γ. Debe ser > 1.
    gas_constant : float
        Constante específica del gas R [J/(kg·K)]. Debe ser > 0.
    total_temperature_k : float
        Temperatura de remanso T₀ [K]. Debe ser > static_temperature_k.
    static_temperature_k : float
        Temperatura estática T [K]. Debe ser > 0.

    Retorna
    -------
    float
        Velocidad del flujo V [m/s].

    Excepciones
    -----------
    ValueError
        Si algún argumento viola su restricción.
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
    # V = √(2γR ΔT / (γ-1))  —  ecuación de energía para gas caloricamente perfecto
    return math.sqrt(2.0 * gamma * gas_constant * delta_t / (gamma - 1.0))


def calculate_mach_from_pressure_ratio(
    total_pressure_kpa: float,
    static_pressure_kpa: float,
    gamma: float,
) -> float:
    """Calcula el número de Mach a partir de la razón de presión total a estática.

    Supuestos
    ---------
    - Flujo isentrópico de un gas caloricamente perfecto.
    - P₀ ≥ P (la presión total siempre es mayor o igual a la estática).

    Fórmula
    -------
    M = √{ (2/(γ-1)) × [(P₀/P)^((γ-1)/γ) - 1] }

    Es la inversión algebraica de la relación isentrópica:
    P₀/P = [1 + (γ-1)/2 · M²]^(γ/(γ-1))

    Para P₀ = P (punto de remanso) la razón es 1, el argumento de la raíz es 0
    y por tanto M = 0, que es la solución físicamente correcta.

    Parámetros
    ----------
    total_pressure_kpa : float
        Presión de remanso P₀ [kPa]. Debe ser > 0.
    static_pressure_kpa : float
        Presión estática local P [kPa]. Debe ser > 0.
    gamma : float
        Razón de calores específicos γ. Debe ser > 1.

    Retorna
    -------
    float
        Número de Mach M (adimensional).

    Excepciones
    -----------
    ValueError
        Si algún argumento viola su restricción o P₀ < P.
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
    # M = √{(2/(γ-1)) × [(P₀/P)^((γ-1)/γ) - 1]}
    return math.sqrt(
        (2.0 / (gamma - 1.0)) * (pressure_ratio ** ((gamma - 1.0) / gamma) - 1.0)
    )


def analyze_nozzle(inputs: NozzleInputs) -> NozzleResults:
    """Ejecuta un análisis isentrópico 1-D completo de la tobera.

    Determina si la garganta está ahogada, calcula las condiciones de salida
    (temperatura, presión, velocidad, Mach) y el empuje bruto de la tobera.

    Supuestos
    ---------
    - Flujo isentrópico 1-D estacionario.
    - Gas caloricamente perfecto.
    - Sin pérdidas de calor hacia la pared (proceso adiabático).

    Parámetros
    ----------
    inputs : NozzleInputs
        Condiciones de remanso, geometría y propiedades del gas.

    Retorna
    -------
    NozzleResults
        Todas las magnitudes calculadas en el plano de salida.
    """
    pass
