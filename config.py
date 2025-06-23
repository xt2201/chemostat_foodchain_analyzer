# config.py
# Central repository for model parameters

# Using Holling Type II / Michaelis-Menten functional responses
# g_i(u) = (m_i * u) / (K_i + u)

def get_params(name="stable_coexistence"):
    """
    Returns a dictionary of parameters for a named scenario.
    a_i = (D + epsilon_i) / D, where D is the dilution rate.
    We work directly with the scaled removal rates a_i.
    """
    
    if name == "stable_coexistence":
        # Parameters leading to a stable E3
        return {
            "m1": 2.0, "K1": 0.5, "a1": 1.0,
            "m2": 0.5, "K2": 0.1, "a2": 0.2,
            "m3": 0.3, "K3": 0.05,"a3": 0.1,
        }
    elif name == "truly_stable":
        # A parameter set GUARANTEED to have a stable E3 for sensitivity analysis.
        # Note max Re(lambda) will be negative.
        return {
            "m1": 2.5, "K1": 0.5, "a1": 1.0,
            "m2": 0.8, "K2": 0.2, "a2": 0.2,
            "m3": 0.5, "K3": 0.15,"a3": 0.15, # Increased K3 and a3 to stabilize the system
        }    
    elif name == "oscillations":
        # Parameters leading to a limit cycle around an unstable E3 (Hopf)
        return {
            "m1": 2.0, "K1": 0.6, "a1": 0.8,
            "m2": 0.6, "K2": 0.1, "a2": 0.1,
            "m3": 0.35,"K3": 0.05,"a3": 0.05,
        }
    elif name == "robust_coexistence":
        # A parameter set specifically for sensitivity analysis where E3 is
        # guaranteed to exist and be stable.
        return {
            "m1": 2.5, "K1": 0.5, "a1": 1.0,  # Strong prey growth
            "m2": 0.8, "K2": 0.2, "a2": 0.2,  # Efficient Predator 1
            "m3": 0.5, "K3": 0.1, "a3": 0.1,  # Efficient Predator 2
        }    
    elif name == "tame_oscillations":
        # A less "violent" oscillatory scenario, better for bifurcation analysis.
        # Interactions are slightly weaker than the main "oscillations" set.
        return {
            "m1": 2.0, "K1": 0.6, "a1": 0.8,
            "m2": 0.4, "K2": 0.2, "a2": 0.1,  # Weaker Predator 1
            "m3": 0.2, "K3": 0.1, "a3": 0.05, # Weaker Predator 2
        }
    elif name == "prey_predator":
        # Parameters where E2 is stable (top predator dies out)
        return {
            "m1": 2.0, "K1": 0.5, "a1": 1.0,
            "m2": 0.5, "K2": 0.1, "a2": 0.2,
            "m3": 0.1, "K3": 0.5, "a3": 0.2, # Top predator is inefficient and cannot survive
        }
    # --- END OF MISSING BLOCK ---
    elif name == "prey_only":
        # Parameters where E1 is stable (predators die out)
        return {
            "m1": 2.0, "K1": 0.5, "a1": 1.0,
            "m2": 0.1, "K2": 0.5, "a2": 0.3, # Predator 1 is inefficient and cannot survive
            "m3": 0.3, "K3": 0.05,"a3": 0.1,
        }
    elif name == "washout":
        # Parameters where E0 is stable
        return {
            "m1": 0.8, "K1": 0.5, "a1": 1.0, # Prey cannot survive
            "m2": 0.5, "K2": 0.1, "a2": 0.2,
            "m3": 0.3, "K3": 0.05,"a3": 0.1,
        }
    else:
        raise ValueError(f"Unknown parameter set name: {name}")