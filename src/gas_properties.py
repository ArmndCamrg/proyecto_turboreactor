"""Propiedades termodinámicas del gas para el análisis de toberas de turbofán.

Supuestos físicos generales del módulo
---------------------------------------
- Gas caloricamente perfecto: γ y Cp se tratan como constantes a una temperatura dada.
- Gas ideal: la ecuación de estado es P = ρ R T (sin correcciones de compresibilidad real).
- Se trabaja con la constante específica del gas R = Rᵤ / M_molar [J/(kg·K)].
  Para aire seco: R ≈ 287.05 J/(kg·K).
"""

import math
from dataclasses import dataclass


@dataclass
class GasProperties:
    """Contenedor de propiedades termodinámicas de un gas.

    Agrupa los parámetros que caracterizan completamente a un gas caloricamente
    perfecto para cálculos de flujo compresible.

    Atributos
    ---------
    gamma : float
        Razón de calores específicos γ = Cp / Cv (adimensional).
        Aire a temperatura ambiente: ~1.4.
        Gases de combustión calientes: ~1.30–1.35.
    R : float
        Constante específica del gas [J/(kg·K)].
        Relacionada con la constante universal: R = Rᵤ / M_molar.
    Cp : float
        Calor específico a presión constante [J/(kg·K)].
    Cv : float
        Calor específico a volumen constante [J/(kg·K)].
        Relación termodinámica: Cv = Cp - R.
    name : str
        Identificador del gas (informativo).
    """
    gamma: float       # razón de calores específicos Cp/Cv
    R: float           # constante específica del gas [J/(kg·K)]
    Cp: float          # calor específico a presión constante [J/(kg·K)]
    Cv: float          # calor específico a volumen constante [J/(kg·K)]
    name: str = "air"


def get_air_properties(T: float = 300.0) -> GasProperties:
    """Devuelve las propiedades estándar del aire seco a una temperatura dada.

    Supuestos
    ---------
    - Aire seco tratado como gas caloricamente perfecto.
    - Las propiedades se evalúan a temperatura estática T.

    Parámetros
    ----------
    T : float
        Temperatura estática [K]. Valor de referencia: 300 K.

    Retorna
    -------
    GasProperties
        Propiedades del aire seco a la temperatura indicada.
    """
    pass


def get_combustion_gas_properties(FAR: float, T: float = 1200.0) -> GasProperties:
    """Devuelve propiedades aproximadas de gases de combustión dado el FAR.

    Supuestos
    ---------
    - Mezcla homogénea de productos de combustión de queroseno.
    - γ y Cp se estiman en función de FAR y temperatura mediante correlaciones
      empíricas simplificadas (aproximación para análisis preliminar).

    Parámetros
    ----------
    FAR : float
        Relación combustible-aire en masa (adimensional).
        Rango típico en turbofán: 0.02–0.04.
    T : float
        Temperatura estática [K]. Referencia: 1200 K.

    Retorna
    -------
    GasProperties
        Propiedades aproximadas de la mezcla de gases calientes.
    """
    pass


def calculate_density(
    pressure_kpa: float,
    temperature_k: float,
    gas_constant: float,
) -> float:
    """Calcula la densidad del gas a partir de la ecuación de estado del gas ideal.

    Supuestos
    ---------
    - Gas ideal: P = ρ R T  →  ρ = P / (R T).
    - No se aplican factores de compresibilidad (Z = 1).

    Fórmula
    -------
    ρ = (pressure_kpa × 1000) / (R × T)

    Donde el factor 1000 convierte kPa a Pa para obtener ρ en kg/m³.

    Parámetros
    ----------
    pressure_kpa : float
        Presión estática [kPa]. Debe ser > 0.
    temperature_k : float
        Temperatura estática [K]. Debe ser > 0.
    gas_constant : float
        Constante específica del gas R [J/(kg·K)]. Debe ser > 0.

    Retorna
    -------
    float
        Densidad ρ [kg/m³].

    Excepciones
    -----------
    ValueError
        Si cualquier argumento no es estrictamente positivo.
    """
    if pressure_kpa <= 0:
        raise ValueError(f"pressure_kpa must be > 0, got {pressure_kpa}.")
    if temperature_k <= 0:
        raise ValueError(f"temperature_k must be > 0, got {temperature_k}.")
    if gas_constant <= 0:
        raise ValueError(f"gas_constant must be > 0, got {gas_constant}.")

    # Conversión de unidades: 1 kPa = 1000 Pa
    pressure_pa = pressure_kpa * 1000.0
    # Ley del gas ideal: ρ = P / (R T)
    return pressure_pa / (gas_constant * temperature_k)


def calculate_speed_of_sound(
    gamma: float,
    gas_constant: float,
    temperature_k: float,
) -> float:
    """Calcula la velocidad del sonido en un gas caloricamente perfecto.

    Supuestos
    ---------
    - Gas caloricamente perfecto con γ constante.
    - Propagación isentrópica de ondas de presión.

    Fórmula
    -------
    a = √(γ R T)

    Esta expresión se obtiene de la derivada isentrópica de la presión respecto
    a la densidad: a² = (∂P/∂ρ)_s = γ R T.

    Parámetros
    ----------
    gamma : float
        Razón de calores específicos γ (adimensional). Debe ser > 1.
    gas_constant : float
        Constante específica del gas R [J/(kg·K)]. Debe ser > 0.
    temperature_k : float
        Temperatura estática T [K]. Debe ser > 0.

    Retorna
    -------
    float
        Velocidad del sonido a [m/s].

    Excepciones
    -----------
    ValueError
        Si algún argumento viola su restricción.
    """
    if gamma <= 1:
        raise ValueError(f"gamma must be > 1, got {gamma}.")
    if gas_constant <= 0:
        raise ValueError(f"gas_constant must be > 0, got {gas_constant}.")
    if temperature_k <= 0:
        raise ValueError(f"temperature_k must be > 0, got {temperature_k}.")

    # a = √(γ R T)
    return math.sqrt(gamma * gas_constant * temperature_k)


def calculate_cp_air(temperature_k: float) -> float:
    """Estima el Cp del aire mediante una aproximación lineal alrededor de 300 K.

    Supuestos
    ---------
    - Aire seco tratado como gas imperfecto con dependencia lineal de Cp con T.
    - La pendiente de 0.1 J/(kg·K²) es una simplificación válida en el rango
      200–1500 K para análisis de ciclos preliminares.
    - No es válida para temperaturas de disociación (> 2500 K).

    Fórmula
    -------
    Cp(T) = 1005 + 0.1 × (T - 300)   [J/(kg·K)]

    Referencia: Cp del aire estándar a 300 K ≈ 1005 J/(kg·K).

    Parámetros
    ----------
    temperature_k : float
        Temperatura estática T [K]. Debe ser > 0.

    Retorna
    -------
    float
        Calor específico a presión constante Cp [J/(kg·K)].

    Excepciones
    -----------
    ValueError
        Si temperature_k <= 0.
    """
    if temperature_k <= 0:
        raise ValueError(f"temperature_k must be > 0, got {temperature_k}.")
    # Cp lineal: valor de referencia 1005 J/(kg·K) a 300 K, con pendiente 0.1 J/(kg·K²)
    return 1005.0 + 0.1 * (temperature_k - 300.0)


def calculate_gamma(cp: float, gas_constant: float) -> float:
    """Calcula la razón de calores específicos γ a partir de Cp y R.

    Supuestos
    ---------
    - Gas caloricamente perfecto: Cv = Cp - R  (relación de Mayer).
    - Cp y R se evalúan a la misma temperatura.

    Fórmulas
    --------
    Cv = Cp - R          (relación de Mayer para gas ideal)
    γ  = Cp / Cv = Cp / (Cp - R)

    La condición Cp > R garantiza Cv > 0 y γ > 1, físicamente requerido
    para que la velocidad del sonido sea real.

    Parámetros
    ----------
    cp : float
        Calor específico a presión constante Cp [J/(kg·K)]. Debe ser > R.
    gas_constant : float
        Constante específica del gas R [J/(kg·K)]. Debe ser > 0.

    Retorna
    -------
    float
        Razón de calores específicos γ (adimensional).

    Excepciones
    -----------
    ValueError
        Si gas_constant <= 0 o cp <= gas_constant.
    """
    if gas_constant <= 0:
        raise ValueError(f"gas_constant must be > 0, got {gas_constant}.")
    if cp <= gas_constant:
        raise ValueError(
            f"cp ({cp}) must be greater than gas_constant ({gas_constant})."
        )
    # γ = Cp / (Cp - R)  derivado de la relación de Mayer
    return cp / (cp - gas_constant)


def speed_of_sound(gamma: float, R: float, T: float) -> float:
    """Calcula la velocidad del sonido en un gas caloricamente perfecto.

    Función de compatibilidad — se prefiere `calculate_speed_of_sound`
    para uso nuevo, ya que incluye validaciones de entrada.

    Supuestos
    ---------
    - Gas caloricamente perfecto con γ constante.

    Fórmula
    -------
    a = √(γ R T)

    Parámetros
    ----------
    gamma : float
        Razón de calores específicos γ (adimensional).
    R : float
        Constante específica del gas [J/(kg·K)].
    T : float
        Temperatura estática [K].

    Retorna
    -------
    float
        Velocidad del sonido a [m/s].
    """
    pass
