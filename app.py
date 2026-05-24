"""Calculadora de propiedades termodinámicas para toberas de turbofán — MVP local.

Análisis y cálculo de sistemas convergentes–divergentes de un turborreactor
de un avión comercial, considerando ecuaciones de estado y calores específicos
dependientes de la altura y presión atmosférica.

Institución : Instituto Politécnico Nacional
Escuela     : ESIME Azcapotzalco
Carrera     : Ingeniería Mecánica
Periodo     : 2026-1
Versión     : v1.0 MVP Académico

Estudiantes
-----------
- Pérez López José Raúl
- Escobedo Guerrero Oscar David

Modelo físico
-------------
- Flujo isentrópico 1-D estacionario.
- Gas caloricamente perfecto (γ y R constantes).
- Mach calculado dinámicamente: M = f(P₀/P, γ), sin valor fijo de usuario.
- Temperatura estática: T = T₀ / [1 + (γ-1)/2 · M²].
- Velocidad: V = √[2γR(T₀-T)/(γ-1)].
- Densidad: ρ = P/(RT)  (ley del gas ideal).
- Área transversal: A = ṁ/(ρV)  (ecuación de continuidad).
- Radio equivalente: R = √(A/π)  (sección transversal circular equivalente).

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
    page_title="Análisis Toberas Turborreactor — IPN ESIME",
    page_icon="✈",
    layout="wide",
)

# ── Estilos CSS institucionales ───────────────────────────────────────────────
# Paleta sobria basada en la identidad gráfica del IPN:
#   guinda  #7B0D28   — color institucional principal
#   gris oscuro  #2C2C2C  — textos principales
#   gris medio   #555555  — textos secundarios
#   fondo neutro #F7F7F7  — tarjetas y fondos alternos

st.markdown("""
<style>
/*
 * REGLA: todos los selectores usan clases propias (.ipn-*).
 * NO se tocan: html, body, div, span, button, input, label,
 * section, [data-testid], [class*="st-"] ni ningún elemento
 * nativo de Streamlit.
 */

/* --- Header institucional -------------------------------------------------- */
.ipn-header {
    text-align: center;
    padding: 0.4rem 1.5rem;
    font-family: "Segoe UI", Arial, sans-serif;
}
.ipn-header-title {
    font-size: 1.0rem;
    font-weight: 700;
    color: #2C2C2C;
    line-height: 1.5;
    margin: 0 0 0.5rem 0;
    font-family: "Segoe UI", Arial, sans-serif;
}
.ipn-header-subtitle {
    font-size: 0.82rem;
    color: #555555;
    margin: 0;
    letter-spacing: 0.01em;
    font-family: "Segoe UI", Arial, sans-serif;
}

/* --- Barra de identidad institucional -------------------------------------- */
.ipn-barra {
    background: linear-gradient(90deg, #7B0D28 0%, #A01830 50%, #7B0D28 100%);
    height: 4px;
    border-radius: 2px;
    margin: 0.8rem 0 1.2rem 0;
}

/* --- Tarjeta de disclaimer ------------------------------------------------- */
.ipn-disclaimer {
    background-color: #FFFDE7;
    border-left: 4px solid #F9A825;
    border-radius: 4px;
    padding: 0.75rem 1rem;
    font-size: 0.83rem;
    font-family: "Segoe UI", Arial, sans-serif;
    color: #4A4A4A;
    margin-bottom: 1.2rem;
    line-height: 1.5;
}

/* --- Tarjeta de supuestos del modelo --------------------------------------- */
.ipn-supuestos {
    background-color: #F7F7F7;
    border-left: 4px solid #7B0D28;
    border-radius: 4px;
    padding: 0.85rem 1.1rem;
    font-size: 0.83rem;
    font-family: "Segoe UI", Arial, sans-serif;
    color: #333333;
    margin-bottom: 1.2rem;
    line-height: 1.55;
}
.ipn-supuestos-titulo {
    display: block;
    margin: 0 0 0.55rem 0;
    font-size: 0.82rem;
    color: #7B0D28;
    text-transform: uppercase;
    letter-spacing: 0.06em;
    font-weight: 700;
    font-family: "Segoe UI", Arial, sans-serif;
}
.ipn-supuestos ul {
    margin: 0;
    padding-left: 1.3rem;
}
.ipn-supuestos li {
    margin-bottom: 0.25rem;
}

/* --- Footer institucional -------------------------------------------------- */
.ipn-footer {
    text-align: center;
    font-size: 0.78rem;
    font-family: "Segoe UI", Arial, sans-serif;
    color: #888888;
    padding: 0.8rem 0 0.3rem 0;
    border-top: 1px solid #E0E0E0;
    margin-top: 1.5rem;
    line-height: 1.6;
}
.ipn-footer strong {
    color: #555555;
}
</style>
""", unsafe_allow_html=True)

# ── Header institucional ──────────────────────────────────────────────────────
# Disposición: logo ESIME | título del proyecto | logo IPN

col_logo_l, col_title, col_logo_r = st.columns([1, 5, 1])

with col_logo_l:
    st.image("assets/logos/esime.png", use_container_width=True)

with col_title:
    st.markdown("""
    <div class="ipn-header">
        <p class="ipn-header-title">
            Análisis y cálculo de sistemas convergentes&thinsp;–&thinsp;divergentes
            de un turborreactor de un avión comercial, considerando ecuaciones de
            estado y calores específicos dependientes de la altura y presión atmosférica
        </p>
        <p class="ipn-header-subtitle">
            Instituto Politécnico Nacional &nbsp;·&nbsp;
            ESIME Azcapotzalco &nbsp;·&nbsp;
            Ingeniería Mecánica &nbsp;·&nbsp;
            Periodo 2026-1
        </p>
    </div>
    """, unsafe_allow_html=True)

with col_logo_r:
    st.image("assets/logos/ipn.png", use_container_width=True)

# Línea guinda de identidad institucional
st.markdown('<div class="ipn-barra"></div>', unsafe_allow_html=True)

# ── Disclaimer técnico ────────────────────────────────────────────────────────
# Visible siempre, antes de cualquier resultado.
st.markdown("""
<div class="ipn-disclaimer">
    ⚠️&nbsp;&nbsp;<strong>Aviso académico:</strong>
    Este software implementa un modelo isentrópico simplificado.
    Los resultados obtenidos son <strong>aproximaciones académicas</strong> y
    no deben utilizarse para certificación aeronáutica, diseño operacional real
    ni toma de decisiones de seguridad.
</div>
""", unsafe_allow_html=True)

# ── Panel lateral: parámetros de entrada ─────────────────────────────────────

with st.sidebar:
    # --- Acerca del proyecto --------------------------------------------------
    with st.expander("📋 Acerca del proyecto", expanded=False):
        st.markdown("""
**Objetivo**

Analizar el comportamiento termodinámico del flujo a lo largo de una tobera
convergente-divergente de turborreactor mediante relaciones isentrópicas
simplificadas para flujo compresible 1-D.

---

**Estudiantes**
- Pérez López José Raúl
- Escobedo Guerrero Oscar David

**Institución**
Instituto Politécnico Nacional

**Escuela**
ESIME Azcapotzalco

**Carrera**
Ingeniería Mecánica

**Periodo**
2026-1

**Versión**
v1.0 MVP Académico
        """)

    st.divider()

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

# ── Supuestos del modelo ──────────────────────────────────────────────────────
# Siempre visible; contextualiza los resultados antes de que el usuario los lea.

st.markdown("""
<div class="ipn-supuestos">
    <span class="ipn-supuestos-titulo">Supuestos del modelo</span>
    <ul>
        <li><strong>Flujo compresible ideal</strong> — relaciones isentrópicas para
            flujo 1-D estacionario en tobera de sección variable.</li>
        <li><strong>Modelo isentrópico simplificado</strong> — proceso adiabático y
            sin irreversibilidades (sin fricción ni ondas de choque).</li>
        <li><strong>Gas ideal</strong> — γ y R constantes a lo largo del análisis
            (gas caloricamente perfecto).</li>
        <li><strong>Sección transversal circular equivalente</strong> — el radio se
            obtiene de R = √(A/π); aplica exclusivamente a toberas de revolución.</li>
        <li><strong>Sin pérdidas viscosas</strong> — no se modelan efectos de capa
            límite ni fricción con la pared.</li>
        <li><strong>Sin transferencia de calor</strong> — proceso completamente
            adiabático en toda la tobera.</li>
        <li><em>Los resultados tienen fines académicos y no constituyen diseño certificable.</em></li>
    </ul>
</div>
""", unsafe_allow_html=True)

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
        # de salida donde la presión es mínima), las condiciones en la entrada
        # y el radio equivalente en la sección de salida.
        col1, col2, col3, col4, col5 = st.columns(5)
        col1.metric("Mach máximo",              f"{df['mach_number'].max():.4f}")
        col2.metric("Velocidad máxima [m/s]",   f"{df['velocity_m_s'].max():.2f}")
        col3.metric("Densidad inicial [kg/m³]",  f"{df['density_kg_m3'].iloc[0]:.4f}")
        col4.metric("Área final [m²]",           f"{df['flow_area_m2'].iloc[-1]:.6f}")
        col5.metric("Radio final [m]",           f"{df['radius_m'].iloc[-1]:.6f}")

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
            (
                "radius_m",
                "Radio equivalente [m]",
                "Radio equivalente vs presión",
            ),
        ]

        # Nota sobre el radio equivalente
        st.caption(
            "El radio se calcula a partir del área suponiendo una sección "
            "transversal circular."
        )

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

st.markdown("""
<div class="ipn-footer">
    <strong>Proyecto académico</strong> desarrollado en
    ESIME Azcapotzalco – Instituto Politécnico Nacional.
    Uso educativo y de investigación.<br>
    Desarrollado con Python, Streamlit, NumPy, Pandas y Plotly.
</div>
""", unsafe_allow_html=True)
