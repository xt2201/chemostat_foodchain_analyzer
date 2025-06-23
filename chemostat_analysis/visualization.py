# chemostat_analysis/visualization.py
import matplotlib.pyplot as plt
import numpy as np
import os

def plot_time_series(sol, title="Chemostat Dynamics", save_path=None):
    """
    Plots the time series of all four state variables from a simulation result.
    If save_path is provided, saves the figure to that path.

    Args:
        sol (scipy.integrate.OdeSolution): The solution object from run_simulation.
        title (str): The title for the plot.
        save_path (str, optional): The full file path to save the figure. Defaults to None.
    """
    t = sol.t
    S, x, y, z = sol.y
    
    fig, ax = plt.subplots(figsize=(12, 7))
    ax.plot(t, S, label="S(t) - Nutrient", lw=2.5, alpha=0.8)
    ax.plot(t, x, label="x(t) - Prey", lw=2.5, alpha=0.8)
    ax.plot(t, y, label="y(t) - Predator 1", lw=2.5, alpha=0.8)
    ax.plot(t, z, label="z(t) - Predator 2", lw=2.5, alpha=0.8)
    
    ax.set_xlabel("Time", fontsize=14)
    ax.set_ylabel("Concentration", fontsize=14)
    ax.set_title(title, fontsize=16, fontweight='bold')
    ax.legend(fontsize=12, loc='upper right')
    ax.grid(True, which='both', linestyle='--', linewidth=0.5)
    ax.set_xlim(t[0], t[-1])
    ax.tick_params(axis='both', which='major', labelsize=12)
    plt.tight_layout()

    # --- ADDED SAVE LOGIC ---
    if save_path:
        # Ensure the directory exists
        os.makedirs(os.path.dirname(save_path), exist_ok=True)
        plt.savefig(save_path, dpi=300, bbox_inches='tight')
        print(f"Plot saved to: {save_path}")
    
    plt.show()

def plot_phase_portrait(sol, dims=['x', 'y', 'z'], title="Phase Portrait", save_path=None):
    """
    Plots a 3D or 2D phase portrait of the trajectory.
    If save_path is provided, saves the figure to that path.

    Args:
        sol (scipy.integrate.OdeSolution): The solution object.
        dims (list): A list of 2 or 3 strings from {'S', 'x', 'y', 'z'}.
        title (str): The title for the plot.
        save_path (str, optional): The full file path to save the figure. Defaults to None.
    """
    dim_map = {'S': 0, 'x': 1, 'y': 2, 'z': 3}
    
    fig = plt.figure(figsize=(10, 8))
    
    if len(dims) == 3:
        ax = fig.add_subplot(111, projection='3d')
        idx1, idx2, idx3 = [dim_map[d] for d in dims]
        
        ax.plot(sol.y[idx1], sol.y[idx2], sol.y[idx3], lw=1.5, color='dodgerblue')
        ax.scatter(sol.y[idx1, 0], sol.y[idx2, 0], sol.y[idx3, 0], c='green', s=80, marker='o', label='Start', depthshade=False)
        ax.scatter(sol.y[idx1, -1], sol.y[idx2, -1], sol.y[idx3, -1], c='red', s=80, marker='X', label='End', depthshade=False)
        
        ax.set_xlabel(f"{dims[0]} Concentration", fontsize=12)
        ax.set_ylabel(f"{dims[1]} Concentration", fontsize=12)
        ax.set_zlabel(f"{dims[2]} Concentration", fontsize=12)

    elif len(dims) == 2:
        ax = fig.add_subplot(111)
        idx1, idx2 = [dim_map[d] for d in dims]
        ax.plot(sol.y[idx1], sol.y[idx2], lw=1.5, color='dodgerblue')
        ax.scatter(sol.y[idx1, 0], sol.y[idx2, 0], c='green', s=80, marker='o', label='Start')
        ax.scatter(sol.y[idx1, -1], sol.y[idx2, -1], c='red', s=80, marker='X', label='End')
        ax.set_xlabel(f"{dims[0]} Concentration", fontsize=12)
        ax.set_ylabel(f"{dims[1]} Concentration", fontsize=12)
        ax.grid(True, which='both', linestyle='--', linewidth=0.5)
    
    else:
        raise ValueError("dims must be a list of 2 or 3 variable names.")

    ax.set_title(title, fontsize=16, fontweight='bold')
    ax.legend(fontsize=12)
    plt.tight_layout()

    # --- ADDED SAVE LOGIC ---
    if save_path:
        os.makedirs(os.path.dirname(save_path), exist_ok=True)
        plt.savefig(save_path, dpi=300, bbox_inches='tight')
        print(f"Plot saved to: {save_path}")

    plt.show()

def plot_bifurcation_diagram(bifurcation_data, param_name, save_path=None):
    """
    Plots a bifurcation diagram from pre-computed data.

    Args:
        bifurcation_data (np.ndarray): Array of shape (N, 3) with [param_val, min, max].
        param_name (str): The name of the bifurcation parameter.
        save_path (str, optional): The full file path to save the figure. Defaults to None.
    """
    fig, ax = plt.subplots(figsize=(12, 7))

    # Plot the min and max bounds
    ax.plot(bifurcation_data[:, 0], bifurcation_data[:, 1], 'k.', markersize=2, alpha=0.6)
    ax.plot(bifurcation_data[:, 0], bifurcation_data[:, 2], 'k.', markersize=2, alpha=0.6)

    ax.set_xlabel(f"Bifurcation Parameter: ${param_name}$", fontsize=14)
    ax.set_ylabel("Long-term z concentration (min/max)", fontsize=14)
    ax.set_title(f"Bifurcation Diagram for Top Predator (z)", fontsize=16, fontweight='bold')
    ax.grid(True, linestyle='--', alpha=0.6)

    # --- ADDED SAVE LOGIC ---
    if save_path:
        os.makedirs(os.path.dirname(save_path), exist_ok=True)
        plt.savefig(save_path, dpi=300, bbox_inches='tight')
        print(f"Plot saved to: {save_path}")

    plt.show()