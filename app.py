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
st.caption("1-D isentropic flow analysis · MVP local")

# ── Sidebar: inputs ───────────────────────────────────────────────────────────

with st.sidebar:
    st.header("Pressure Range")
    inlet_pressure_kpa = st.number_input(
        "Inlet Pressure [kPa]", min_value=0.1, max_value=10_000.0,
        value=1400.0, step=10.0,
    )
    outlet_pressure_kpa = st.number_input(
        "Outlet Pressure [kPa]", min_value=0.1, max_value=10_000.0,
        value=101.325, step=1.0,
    )
    num_points = st.number_input(
        "Number of Points", min_value=2, max_value=100_000,
        value=12986, step=1,
    )

    st.header("Flow Conditions")
    temperature_k = st.number_input(
        "Temperature [K]", min_value=1.0, max_value=5000.0,
        value=1200.0, step=10.0,
    )
    mass_flow_rate = st.number_input(
        "Mass Flow Rate [kg/s]", min_value=0.001, max_value=10_000.0,
        value=250.0, step=1.0,
    )
    mach_number = st.number_input(
        "Mach Number", min_value=0.0, max_value=10.0,
        value=0.3, step=0.01, format="%.3f",
    )

    st.header("Gas Properties")
    gamma = st.number_input(
        "Specific Heat Ratio γ", min_value=1.01, max_value=2.0,
        value=1.33, step=0.01, format="%.3f",
    )
    gas_constant = st.number_input(
        "Gas Constant R [J/(kg·K)]", min_value=1.0, max_value=1000.0,
        value=287.0, step=1.0,
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
            mach_number=mach_number,
            mass_flow_rate=mass_flow_rate,
        )

        # ── Metrics ───────────────────────────────────────────────────────────
        col1, col2, col3, col4 = st.columns(4)
        col1.metric("Velocidad [m/s]", f"{df['velocity_m_s'].iloc[0]:.2f}")
        col2.metric("Mach promedio", f"{df['mach_number'].mean():.4f}")
        col3.metric("Densidad inicial [kg/m³]", f"{df['density_kg_m3'].iloc[0]:.4f}")
        col4.metric("Área final [m²]", f"{df['flow_area_m2'].iloc[-1]:.6f}")

        st.divider()

        # ── Table preview ─────────────────────────────────────────────────────
        st.subheader("Primeras filas del resultado")
        st.dataframe(df.head(20), use_container_width=True)

        # ── CSV download ──────────────────────────────────────────────────────
        st.download_button(
            label="Descargar CSV",
            data=df.to_csv(index=False).encode("utf-8"),
            file_name="turbofan_nozzle_results.csv",
            mime="text/csv",
            use_container_width=True,
        )

        st.divider()

        # ── Charts ────────────────────────────────────────────────────────────
        st.subheader("Gráficas")

        charts = [
            ("velocity_m_s",    "Velocidad [m/s]",      "Presión vs Velocidad"),
            ("mach_number",     "Número de Mach",       "Presión vs Mach"),
            ("density_kg_m3",   "Densidad [kg/m³]",     "Presión vs Densidad"),
            ("flow_area_m2",    "Área de flujo [m²]",   "Presión vs Área de flujo"),
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
