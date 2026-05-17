"""Visualization helpers for nozzle flow results."""

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
    """Plot Mach number distribution along the nozzle axis.

    Args:
        x: axial positions [m].
        mach: Mach number at each position.
        title: plot title.

    Returns:
        Matplotlib Figure.
    """
    pass


def plot_pressure_profile(
    x: np.ndarray,
    pressure: np.ndarray,
    P_amb: Optional[float] = None,
    title: str = "Static Pressure Profile",
) -> Figure:
    """Plot static pressure distribution along the nozzle axis.

    Args:
        x: axial positions [m].
        pressure: static pressure [Pa] at each position.
        P_amb: ambient pressure to draw as a reference line [Pa].
        title: plot title.

    Returns:
        Matplotlib Figure.
    """
    pass


def plot_temperature_profile(
    x: np.ndarray,
    temperature: np.ndarray,
    title: str = "Static Temperature Profile",
) -> Figure:
    """Plot static temperature distribution along the nozzle axis.

    Args:
        x: axial positions [m].
        temperature: static temperature [K] at each position.
        title: plot title.

    Returns:
        Matplotlib Figure.
    """
    pass


def create_line_chart(
    df,
    x_column: str,
    y_column: str,
    title: str,
    y_axis_title: str,
) -> go.Figure:
    """Create a Plotly line chart from a DataFrame.

    Args:
        df: pandas DataFrame containing the data.
        x_column: column name for the x-axis. Must exist in df.
        y_column: column name for the y-axis. Must exist in df.
        title: chart title.
        y_axis_title: label for the y-axis.

    Returns:
        Plotly Figure.

    Raises:
        ValueError: if x_column or y_column is not found in df.
    """
    if x_column not in df.columns:
        raise ValueError(f"Column '{x_column}' not found in DataFrame.")
    if y_column not in df.columns:
        raise ValueError(f"Column '{y_column}' not found in DataFrame.")

    fig = px.line(df, x=x_column, y=y_column, title=title)
    fig.update_layout(xaxis_title=x_column, yaxis_title=y_axis_title)
    return fig


def plot_results_summary(results: NozzleResults) -> Figure:
    """Build a summary figure with key exit-plane quantities as a bar/text chart.

    Args:
        results: NozzleResults from analyze_nozzle.

    Returns:
        Matplotlib Figure.
    """
    pass
