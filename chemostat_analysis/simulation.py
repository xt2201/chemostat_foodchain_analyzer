# chemostat_analysis/simulation.py
import numpy as np
from scipy.integrate import solve_ivp
from .model import chemostat_foodchain_ode

def run_simulation(U0, params, t_span, t_eval_count=2000):
    """
    Runs a time-course simulation of the chemostat model.

    Args:
        U0 (np.ndarray): Initial conditions [S0, x0, y0, z0].
        params (dict): Dictionary of model parameters.
        t_span (tuple): The start and end time for the simulation, e.g., (0, 1000).
        t_eval_count (int): The number of time points to evaluate and store.

    Returns:
        scipy.integrate.OdeSolution: The solution object from solve_ivp,
                                     which contains times (sol.t) and states (sol.y).
    """
    t_eval = np.linspace(t_span[0], t_span[1], t_eval_count)
    
    sol = solve_ivp(
        fun=chemostat_foodchain_ode,
        t_span=t_span,
        y0=U0,
        t_eval=t_eval,
        args=(params,),
        # --- THIS IS THE KEY CHANGE ---
        method='LSODA',  # Use a solver suitable for stiff systems
        # -----------------------------
        dense_output=True, # Allows for smooth plotting
        atol=1e-7,      # Absolute tolerance
        rtol=1e-7       # Relative tolerance for high accuracy
    )
    return sol