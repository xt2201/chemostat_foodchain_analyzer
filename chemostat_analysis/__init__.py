# chemostat_analysis/__init__.py

# Expose key functions for easy access from the top-level package
from .model import chemostat_foodchain_ode
from .equilibria import find_equilibria
from .stability import analyze_stability, calculate_jacobian
from .simulation import run_simulation
from .visualization import plot_time_series, plot_phase_portrait

# Define what is imported with 'from chemostat_analysis import *'
__all__ = [
    "chemostat_foodchain_ode",
    "find_equilibria",
    "analyze_stability",
    "calculate_jacobian",
    "run_simulation",
    "plot_time_series",
    "plot_phase_portrait",
]