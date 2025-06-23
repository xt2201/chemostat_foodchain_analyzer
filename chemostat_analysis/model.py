# chemostat_analysis/model.py (This version is robust and correct)
import numpy as np

def g(u, m, K):
    """Holling Type II / Michaelis-Menten functional response."""
    return (m * u) / (K + u)


def g_prime(u, m, K):
    """Derivative of the Holling Type II function with respect to u."""
    if u <= 0:
        return m / K
    return (m * K) / ((K + u)**2)

def chemostat_foodchain_ode(t, U, params):
    """
    The ODE system for the 4-species chemostat model.
    *** FINAL CORRECTED AND ROBUST VERSION ***
    """
    S, x, y, z = U
    
    # Unpack parameters
    m1, K1, a1 = params["m1"], params["K1"], params["a1"]
    m2, K2, a2 = params["m2"], params["K2"], params["a2"]
    m3, K3, a3 = params["m3"], params["K3"], params["a3"]

    # --- Step 1: Calculate interaction terms using non-negative values ---
    S_calc = max(0, S)
    x_calc = max(0, x)
    y_calc = max(0, y)
    z_calc = max(0, z)

    g1_S = g(S_calc, m1, K1)
    g2_x = g(x_calc, m2, K2)
    g3_y = g(y_calc, m3, K3)

    # --- Step 2: Calculate the raw per-capita growth rates ---
    # Avoid division by zero when a population is at or near zero.
    dxdt_raw = g1_S - a1 - (g2_x * y_calc) / x if x > 1e-12 else g1_S - a1
    dydt_raw = g2_x - a2 - (g3_y * z_calc) / y if y > 1e-12 else g2_x - a2
    dzdt_raw = g3_y - a3

    # --- Step 3: Enforce positivity constraint on derivatives ---
    # If a population is negative (a solver artifact), force its derivative to be non-negative.
    
    dxdt = x * dxdt_raw if x > 0 else max(0, dxdt_raw)
    dydt = y * dydt_raw if y > 0 else max(0, dydt_raw)
    dzdt = z * dzdt_raw if z > 0 else max(0, dzdt_raw)
    
    # The S dynamics do not need this special handling as S is not a population
    dSdt = 1 - S - g1_S * x_calc
        
    return np.array([dSdt, dxdt, dydt, dzdt])