"""Funciones de visualización para los resultados del análisis de toberas.

Proporciona gráficas de perfiles axiales (Mach, presión, temperatura) y
resúmenes del plano de salida. Las funciones basadas en Matplotlib devuelven
objetos Figure para uso en entornos de escritorio o exportación; las basadas
en Plotly están diseñadas para uso interactivo en Streamlit.
"""

from typing import Optional
import numpy as np
import matplotlib.pyplot as plt
import plotly.express as px
import plotly.graph_objects as go
from matplotlib.figure import Figure

from src.calculations import NozzleResults


def plot_mach_profile(
    x: np.ndarray,
    mach: np.ndarray,
    title: str = "Mach Number Profile",
) -> Figure:
    """Grafica el perfil axial del número de Mach a lo largo de la tobera.

    El número de Mach aumenta monótonamente en una expansión isentrópica:
    en la garganta alcanza M = 1 y en la tobera divergente supera la unidad
    si el flujo está ahogado y la contrapresión es suficientemente baja.

    Parámetros
    ----------
    x : np.ndarray
        Posiciones axiales a lo largo de la tobera [m].
    mach : np.ndarray
        Número de Mach M en cada posición (adimensional).
        Misma longitud que `x`.
    title : str
        Título de la gráfica.

    Retorna
    -------
    Figure
        Figura de Matplotlib lista para mostrar o exportar.
    """
    pass


def plot_pressure_profile(
    x: np.ndarray,
    pressure: np.ndarray,
    P_amb: Optional[float] = None,
    title: str = "Static Pressure Profile",
) -> Figure:
    """Grafica el perfil axial de presión estática a lo largo de la tobera.

    En flujo isentrópico subsónico la presión disminuye al disminuir el área.
    Si se proporciona P_amb se añade una línea horizontal de referencia, útil
    para visualizar el grado de sobre- o sub-expansión en la salida.

    Parámetros
    ----------
    x : np.ndarray
        Posiciones axiales a lo largo de la tobera [m].
    pressure : np.ndarray
        Presión estática P en cada posición [Pa].
        Misma longitud que `x`.
    P_amb : float, opcional
        Presión ambiente de referencia [Pa]. Si se proporciona, se traza
        como línea horizontal discontinua.
    title : str
        Título de la gráfica.

    Retorna
    -------
    Figure
        Figura de Matplotlib lista para mostrar o exportar.
    """
    pass


def plot_temperature_profile(
    x: np.ndarray,
    temperature: np.ndarray,
    title: str = "Static Temperature Profile",
) -> Figure:
    """Grafica el perfil axial de temperatura estática a lo largo de la tobera.

    La temperatura estática disminuye conforme el gas se acelera, dado que
    la entalpía de remanso se conserva (proceso adiabático) y la energía
    cinética aumenta a expensas de la entalpía estática.

    Parámetros
    ----------
    x : np.ndarray
        Posiciones axiales a lo largo de la tobera [m].
    temperature : np.ndarray
        Temperatura estática T en cada posición [K].
        Misma longitud que `x`.
    title : str
        Título de la gráfica.

    Retorna
    -------
    Figure
        Figura de Matplotlib lista para mostrar o exportar.
    """
    pass


def create_line_chart(
    df,
    x_column: str,
    y_column: str,
    title: str,
    y_axis_title: str,
) -> go.Figure:
    """Crea una gráfica de línea interactiva con Plotly a partir de un DataFrame.

    Diseñada para mostrar perfiles termodinámicos en la interfaz Streamlit.
    El eje x se etiqueta con el nombre de la columna; el eje y usa el título
    descriptivo proporcionado para mayor claridad técnica.

    Parámetros
    ----------
    df : pd.DataFrame
        DataFrame que contiene los datos a graficar. Debe incluir las
        columnas `x_column` e `y_column`.
    x_column : str
        Nombre de la columna del DataFrame para el eje x.
        Debe existir en `df`.
    y_column : str
        Nombre de la columna del DataFrame para el eje y.
        Debe existir en `df`.
    title : str
        Título de la gráfica (aparece en la parte superior).
    y_axis_title : str
        Etiqueta descriptiva del eje y, incluyendo unidades cuando aplique.
        Ejemplo: "Velocidad [m/s]", "Número de Mach [ ]".

    Retorna
    -------
    go.Figure
        Figura interactiva de Plotly lista para renderizar con
        `st.plotly_chart`.

    Excepciones
    -----------
    ValueError
        Si `x_column` o `y_column` no se encuentran en las columnas de `df`.
    """
    if x_column not in df.columns:
        raise ValueError(f"Column '{x_column}' not found in DataFrame.")
    if y_column not in df.columns:
        raise ValueError(f"Column '{y_column}' not found in DataFrame.")

    fig = px.line(df, x=x_column, y=y_column, title=title)
    fig.update_layout(xaxis_title=x_column, yaxis_title=y_axis_title)
    return fig


def plot_results_summary(results: NozzleResults) -> Figure:
    """Genera una figura resumen con las magnitudes clave en el plano de salida.

    Presenta en un gráfico de barras o tabla visual las propiedades más
    relevantes del análisis: Mach de salida, velocidad, temperatura, presión,
    empuje y gasto másico. Útil para reportes o comparaciones de diseños.

    Parámetros
    ----------
    results : NozzleResults
        Resultado del análisis completo producido por `analyze_nozzle`.

    Retorna
    -------
    Figure
        Figura de Matplotlib lista para mostrar o exportar.
    """
    pass
