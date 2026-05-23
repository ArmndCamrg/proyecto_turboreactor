"""Calculadora de propiedades termodinámicas para toberas de turbofán — MVP local.

Interfaz Streamlit que implementa un análisis isentrópico 1-D de una tobera.
El usuario especifica las condiciones de remanso y las propiedades del gas;
la aplicación calcula el número de Mach variable en cada punto a partir de
la razón de presiones P₀/P y presenta los perfiles termodinámicos resultantes.

Modelo físico
-------------
- Flujo isentrópico 1-D estacionario.
- Gas caloricamente perfecto (γ y R constantes).
- Mach calculado dinámicamente: M = f(P₀/P, γ), sin valor fijo de usuario.
- Temperatura estática: T = T₀ / [1 + (γ-1)/2 · M²].
- Velocidad: V = √[2γR(T₀-T)/(γ-1)].
- Densidad: ρ = P/(RT)  (ley del gas ideal).
- Área transversal: A = ṁ/(ρV)  (ecuación de continuidad).

Entradas del usuario
--------------------
- P₀ [kPa] : presión de remanso en la entrada.
- P_salida [kPa] : presión estática en la sección de salida (contrapresión).
- T₀ [K] : temperatura de remanso en la entrada.
- ṁ [kg/s] : gasto másico (constante a lo largo de la tobera).
- γ [-] : razón de calores específicos del gas.
- R [J/(kg·K)] : constante específica del gas.
- N [-] : número de puntos de discretización del rango de presiones.
"""

import streamlit as st

from src.calculations import build_results_table
from src.plotting import create_line_chart, create_normalized_comparison_chart

# ── Configuración de página ───────────────────────────────────────────────────

st.set_page_config(
    page_title="Turbofan Nozzle Calculator",
    page_icon="✈",
    layout="wide",
)

st.title("Turbofan Nozzle — Thermodynamic Properties")
st.caption(
    "Análisis isentrópico 1-D · Mach calculado dinámicamente a partir de "
    "la relación P₀/P en cada punto · MVP local"
)

# ── Panel lateral: parámetros de entrada ─────────────────────────────────────

with st.sidebar:
    # --- Rango de presiones ---------------------------------------------------
    # P₀ es la presión de remanso (condición aguas arriba).
    # P_salida es la presión estática en la descarga (contrapresión).
    # La razón P₀/P_local en cada punto determina el Mach local.
    st.header("Rango de Presión")
    inlet_pressure_kpa = st.number_input(
        "Presión total de entrada P₀ [kPa]",
        min_value=0.1, max_value=10_000.0,
        value=1400.0, step=10.0,
        help="Presión de remanso aguas arriba de la tobera.",
    )
    outlet_pressure_kpa = st.number_input(
        "Presión estática de salida [kPa]",
        min_value=0.1, max_value=10_000.0,
        value=101.325, step=1.0,
        help="Presión ambiente o de descarga.",
    )
    num_points = st.number_input(
        "Número de puntos",
        min_value=2, max_value=100_000,
        value=12986, step=1,
    )

    # --- Condiciones de flujo -------------------------------------------------
    # T₀ es la temperatura de remanso; se conserva a lo largo del flujo isentrópico.
    # ṁ es el gasto másico; se conserva por la ecuación de continuidad.
    st.header("Condiciones de Flujo")
    temperature_k = st.number_input(
        "Temperatura total de entrada T₀ [K]",
        min_value=1.0, max_value=5000.0,
        value=1200.0, step=10.0,
        help="Temperatura de remanso aguas arriba.",
    )
    mass_flow_rate = st.number_input(
        "Gasto másico ṁ [kg/s]",
        min_value=0.001, max_value=10_000.0,
        value=250.0, step=1.0,
    )

    # --- Propiedades del gas --------------------------------------------------
    # γ = Cp/Cv: para gases de combustión calientes se usa ~1.33;
    #            para aire a temperatura ambiente se usa 1.4.
    # R: constante específica del gas; para aire R ≈ 287 J/(kg·K).
    st.header("Propiedades del Gas")
    gamma = st.number_input(
        "Razón de calores específicos γ",
        min_value=1.01, max_value=2.0,
        value=1.33, step=0.01, format="%.3f",
        help="Cp/Cv — usar ~1.33 para gases de combustión, 1.4 para aire.",
    )
    gas_constant = st.number_input(
        "Constante específica del gas R [J/(kg·K)]",
        min_value=1.0, max_value=1000.0,
        value=287.0, step=1.0,
    )

    # Nota informativa: el Mach no es un parámetro de entrada en este modelo
    st.info(
        "El número de Mach se calcula automáticamente en cada punto "
        "mediante la relación isentrópica P₀/P.",
        icon="ℹ",
    )

    run = st.button("Calcular", type="primary", use_container_width=True)

# ── Área principal: resultados ────────────────────────────────────────────────

if run:
    try:
        # Cálculo del DataFrame con todos los perfiles termodinámicos
        df = build_results_table(
            inlet_pressure_kpa=inlet_pressure_kpa,
            outlet_pressure_kpa=outlet_pressure_kpa,
            num_points=int(num_points),
            temperature_k=temperature_k,
            gas_constant=gas_constant,
            gamma=gamma,
            mass_flow_rate=mass_flow_rate,
        )

        # ── Métricas de resumen ───────────────────────────────────────────────
        # Se muestran los valores máximos de Mach y velocidad (en la sección
        # de salida donde la presión es mínima) y las condiciones en la entrada.
        col1, col2, col3, col4 = st.columns(4)
        col1.metric("Mach máximo",             f"{df['mach_number'].max():.4f}")
        col2.metric("Velocidad máxima [m/s]",  f"{df['velocity_m_s'].max():.2f}")
        col3.metric("Densidad inicial [kg/m³]", f"{df['density_kg_m3'].iloc[0]:.4f}")
        col4.metric("Área final [m²]",          f"{df['flow_area_m2'].iloc[-1]:.6f}")

        st.divider()

        # ── Vista previa de la tabla de resultados ────────────────────────────
        # Se muestran las primeras 20 filas; el CSV completo está disponible
        # con el botón de descarga.
        st.subheader("Vista previa de resultados")
        st.dataframe(df.head(20), use_container_width=True)

        # ── Descarga del CSV completo ─────────────────────────────────────────
        st.download_button(
            label="Descargar CSV completo",
            data=df.to_csv(index=False).encode("utf-8"),
            file_name="turbofan_nozzle_results.csv",
            mime="text/csv",
            use_container_width=True,
        )

        st.divider()

        # ── Perfiles termodinámicos ───────────────────────────────────────────
        # Cada gráfica muestra cómo varía una propiedad termodinámica conforme
        # la presión estática disminuye (gas expandiéndose a través de la tobera).
        # El eje x es la presión estática local P [kPa].
        st.subheader("Perfiles termodinámicos a lo largo de la tobera")

        charts = [
            (
                "velocity_m_s",
                "Velocidad [m/s]",
                "Presión estática vs Velocidad de flujo",
            ),
            (
                "mach_number",
                "Número de Mach [ ]",
                "Presión estática vs Número de Mach (isentrópico)",
            ),
            (
                "static_temperature_k",
                "Temperatura estática [K]",
                "Presión estática vs Temperatura estática",
            ),
            (
                "density_kg_m3",
                "Densidad [kg/m³]",
                "Presión estática vs Densidad del gas",
            ),
            (
                "flow_area_m2",
                "Área de flujo [m²]",
                "Presión estática vs Área transversal de flujo",
            ),
        ]

        # Disposición en dos columnas para aprovechar el layout ancho
        col_a, col_b = st.columns(2)
        for i, (y_col, y_label, title) in enumerate(charts):
            fig = create_line_chart(df, "pressure_kpa", y_col, title, y_label)
            target_col = col_a if i % 2 == 0 else col_b
            target_col.plotly_chart(fig, use_container_width=True)

        st.divider()

        # ── Comparación de tendencias ─────────────────────────────────────────
        # Cada propiedad se normaliza a [0, 1] para poder superponerlas en un
        # mismo eje, independientemente de sus unidades originales.
        st.subheader("Comparación de tendencias")
        st.caption(
            "Esta gráfica normaliza las variables entre 0 y 1 para comparar "
            "tendencias, ya que cada propiedad tiene unidades distintas."
        )
        fig_norm = create_normalized_comparison_chart(df)
        st.plotly_chart(fig_norm, use_container_width=True)

    except ValueError as exc:
        # Errores de validación de parámetros (p. ej. P_salida > P₀)
        st.error(f"Error en los parámetros de entrada: {exc}")
    except Exception as exc:
        # Cualquier error inesperado en el cálculo
        st.error(f"Error inesperado: {exc}")

else:
    st.info("Configura los parámetros en el panel lateral y presiona **Calcular**.")

# ── Pie de página ─────────────────────────────────────────────────────────────

st.divider()
st.caption("proyecto_turboreactor · MVP · local only")
