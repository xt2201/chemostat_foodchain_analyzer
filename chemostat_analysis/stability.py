# chemostat_analysis/stability.py
import numpy as np
from .model import g, g_prime

def calculate_jacobian(U, params):
    """
    Analytically calculates the Jacobian matrix of the ODE system at state U.

    Args:
        U (np.ndarray): The state vector [S, x, y, z] at which to linearize.
        params (dict): Dictionary of model parameters.

    Returns:
        np.ndarray: The 4x4 Jacobian matrix.
    """
    S, x, y, z = U
    
    # Unpack parameters
    m1, K1, a1 = params["m1"], params["K1"], params["a1"]
    m2, K2, a2 = params["m2"], params["K2"], params["a2"]
    m3, K3, a3 = params["m3"], params["K3"], params["a3"]

    # Pre-calculate growth rates and their derivatives for efficiency
    g1_S = g(S, m1, K1)
    g1_S_prime = g_prime(S, m1, K1)
    g2_x = g(x, m2, K2)
    g2_x_prime = g_prime(x, m2, K2)
    g3_y = g(y, m3, K3)
    g3_y_prime = g_prime(y, m3, K3)

    # Initialize the Jacobian matrix
    J = np.zeros((4, 4))

    # Row 1: d(dS/dt) / d(S,x,y,z)
    J[0, 0] = -1 - x * g1_S_prime
    J[0, 1] = -g1_S
    
    # Row 2: d(dx/dt) / d(S,x,y,z)
    J[1, 0] = x * g1_S_prime
    J[1, 1] = g1_S - a1 - y * g2_x_prime
    J[1, 2] = -g2_x
    
    # Row 3: d(dy/dt) / d(S,x,y,z)
    J[2, 1] = y * g2_x_prime
    J[2, 2] = g2_x - a2 - z * g3_y_prime
    J[2, 3] = -g3_y

    # Row 4: d(dz/dt) / d(S,x,y,z)
    J[3, 2] = z * g3_y_prime
    J[3, 3] = g3_y - a3
    
    return J

def analyze_stability(U, params):
    """
    Determines the stability of an equilibrium point by analyzing the
    eigenvalues of the Jacobian matrix.

    Args:
        U (np.ndarray): The equilibrium point coordinates.
        params (dict): Dictionary of model parameters.

    Returns:
        tuple: A tuple containing:
            - np.ndarray: The eigenvalues of the Jacobian.
            - str: A string describing the stability ('Stable', 'Unstable', 'Saddle', 'Neutral').
    """
    J = calculate_jacobian(U, params)
    eigenvalues = np.linalg.eigvals(J)
    
    real_parts = np.real(eigenvalues)
    max_real_part = np.max(real_parts)
    min_real_part = np.min(real_parts)
    
    # Use a small tolerance for floating point comparisons
    TOL = 1e-9

    if max_real_part < -TOL:
        stability = "Stable"
    elif min_real_part > TOL:
        stability = "Unstable (Source)"
    elif max_real_part > TOL and min_real_part < -TOL:
        stability = "Unstable (Saddle)"
    else:
        # If max real part is very close to zero, it could be a bifurcation point
        stability = "Neutral (Possible Hopf Bifurcation)"

    return eigenvalues, stability