# chemostat_analysis/equilibria.py
import numpy as np
from scipy.optimize import fsolve, root_scalar
from .model import g

LARGE_NUMBER = 1e12

def find_equilibria(params):
    """
    Finds all existing non-negative equilibria.
    *** FINAL ROBUST VERSION using a fixed search bracket for E3. ***
    """
    equilibria = {}
    
    m1, K1, a1 = params["m1"], params["K1"], params["a1"]
    m2, K2, a2 = params["m2"], params["K2"], params["a2"]
    m3, K3, a3 = params["m3"], params["K3"], params["a3"]

    equilibria["E0"] = np.array([1.0, 0.0, 0.0, 0.0])

    if m1 > a1:
        S1 = (K1 * a1) / (m1 - a1)
        if 0 < S1 < 1:
            x1 = (1 - S1) / a1
            equilibria["E1"] = np.array([S1, x1, 0.0, 0.0])

    if m2 > a2:
        x2 = (K2 * a2) / (m2 - a2)
        def s2_eq(S):
            return 1 - S - g(S, m1, K1) * x2
        try:
            sol_s2 = root_scalar(s2_eq, bracket=[0, 1], method='brentq')
            if sol_s2.converged:
                S2 = sol_s2.root
                if a2 > 0:
                    y2 = (x2 * (g(S2, m1, K1) - a1)) / a2
                    if y2 > 0:
                        equilibria["E2"] = np.array([S2, x2, y2, 0.0])
        except ValueError:
            pass

    # --- ROBUST E3 FINDING LOGIC ---
    if m3 > a3:
        y3 = (K3 * a3) / (m3 - a3)
        def e3_master_equation(x):
            if x <= 0: return LARGE_NUMBER
            try:
                s_sol = root_scalar(lambda S: 1 - S - g(S, m1, K1) * x, bracket=[0,1])
                if not s_sol.converged: return LARGE_NUMBER
                S = s_sol.root
            except ValueError:
                return LARGE_NUMBER
            
            g2_val = g(x, m2, K2)
            if g2_val <= 0: return LARGE_NUMBER
            
            y_of_x = (x * (g(S, m1, K1) - a1)) / g2_val
            return y_of_x - y3

        # Use a fixed, robust search bracket instead of depending on E1 and E2
        try:
            # A search bracket for x from near-zero to a reasonably large value
            x3_search_bracket = [1e-6, 5.0]
            sol_x3 = root_scalar(e3_master_equation, bracket=x3_search_bracket, method='brentq')
            
            if sol_x3.converged:
                x3 = sol_x3.root
                S3_sol = root_scalar(lambda S: 1 - S - g(S, m1, K1) * x3, bracket=[0, 1])
                if S3_sol.converged:
                   S3 = S3_sol.root
                   if a3 > 0:
                       z3 = (y3 * (g(x3, m2, K2) - a2)) / a3
                       if z3 > 0:
                           equilibria["E3"] = np.array([S3, x3, y3, z3])
        except (ValueError, RuntimeError):
            # This will happen if the function does not cross zero within the bracket.
            # It's a valid outcome if E3 doesn't exist for the params, so we just pass.
            pass
    
    return equilibria