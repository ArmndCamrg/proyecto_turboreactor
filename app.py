"""Turbofan Nozzle Thermodynamic Calculator — Streamlit MVP."""

import streamlit as st

from src.calculations import build_results_table
from src.plotting import create_line_chart

# ── Page config ───────────────────────────────────────────────────────────────

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

# ── Sidebar: inputs ───────────────────────────────────────────────────────────

with st.sidebar:
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

    st.info(
        "El número de Mach se calcula automáticamente en cada punto "
        "mediante la relación isentrópica P₀/P.",
        icon="ℹ",
    )

    run = st.button("Calcular", type="primary", use_container_width=True)

# ── Main area ─────────────────────────────────────────────────────────────────

if run:
    try:
        df = build_results_table(
            inlet_pressure_kpa=inlet_pressure_kpa,
            outlet_pressure_kpa=outlet_pressure_kpa,
            num_points=int(num_points),
            temperature_k=temperature_k,
            gas_constant=gas_constant,
            gamma=gamma,
            mass_flow_rate=mass_flow_rate,
        )

        # ── Metrics ───────────────────────────────────────────────────────────
        col1, col2, col3, col4 = st.columns(4)
        col1.metric("Mach máximo",             f"{df['mach_number'].max():.4f}")
        col2.metric("Velocidad máxima [m/s]",  f"{df['velocity_m_s'].max():.2f}")
        col3.metric("Densidad inicial [kg/m³]", f"{df['density_kg_m3'].iloc[0]:.4f}")
        col4.metric("Área final [m²]",          f"{df['flow_area_m2'].iloc[-1]:.6f}")

        st.divider()

        # ── Table preview ─────────────────────────────────────────────────────
        st.subheader("Vista previa de resultados")
        st.dataframe(df.head(20), use_container_width=True)

        # ── CSV download ──────────────────────────────────────────────────────
        st.download_button(
            label="Descargar CSV completo",
            data=df.to_csv(index=False).encode("utf-8"),
            file_name="turbofan_nozzle_results.csv",
            mime="text/csv",
            use_container_width=True,
        )

        st.divider()

        # ── Charts ────────────────────────────────────────────────────────────
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

        col_a, col_b = st.columns(2)
        for i, (y_col, y_label, title) in enumerate(charts):
            fig = create_line_chart(df, "pressure_kpa", y_col, title, y_label)
            target_col = col_a if i % 2 == 0 else col_b
            target_col.plotly_chart(fig, use_container_width=True)

    except ValueError as exc:
        st.error(f"Error en los parámetros de entrada: {exc}")
    except Exception as exc:
        st.error(f"Error inesperado: {exc}")

else:
    st.info("Configura los parámetros en el panel lateral y presiona **Calcular**.")

# ── Footer ────────────────────────────────────────────────────────────────────

st.divider()
st.caption("proyecto_turboreactor · MVP · local only")
