"""Visualization helpers for nozzle flow results."""

from typing import Optional
import numpy as np
import matplotlib.pyplot as plt
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


def plot_results_summary(results: NozzleResults) -> Figure:
    """Build a summary figure with key exit-plane quantities as a bar/text chart.

    Args:
        results: NozzleResults from analyze_nozzle.

    Returns:
        Matplotlib Figure.
    """
    pass
