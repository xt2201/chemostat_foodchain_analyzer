# Chemostat Food Chain Analyzer

This project provides a Python implementation for simulating and analyzing a four-species chemostat food chain model with distinct removal rates.

## Features
- ODE model definition with Holling Type II functional responses.
- Functions to find and classify all equilibrium points.
- Stability analysis via Jacobian linearization and eigenvalue calculation.
- Time-course simulation using SciPy's ODE solvers.
- Visualization tools for time series and phase portraits.

## Project Structure
- `notebooks/`: Jupyter notebooks for experiments and demonstrations.
- `results/`: Directory for saving plots and data.
- `chemostat_analysis/`: Core Python package containing the model and analysis tools.
- `config.py`: Central configuration for model parameters.

## Setup
1. Clone the repository.
```
https://github.com/xt2201/chemostat_foodchain_analyzer.git
```
2. Create a virtual environment (optional but recommended):
   ```bash
   python -m venv venv
   source venv/bin/activate  # On Windows, use `venv\Scripts\activate`
   ```
3. Install the required dependencies: 
      ```bash
      pip install -r requirements.tx
      ```
4. Run the experiments in the notebooks/ directory.
jupyter lab

# Folder Structure

The project directory is organized as follows:

```
chemostat_foodchain_analyzer/
├── notebooks/                  # Jupyter notebooks for experiments, exploration, and visualization.
│   ├── 01_equilibrium_analysis.ipynb
│   ├── 02_time_course_simulation.ipynb
│   ├── 03_bifurcation_diagram.ipynb
│   └── 04_sensitivity_analysis.ipynb
│
├── results/                    # Output folder for plots and data (to be ignored by git).
│   ├── plots/
│   │   ├── time_series/
│   │   └── phase_portraits/
│   │   └── bifurcations/
│   └── data/
│
├── chemostat_analysis/         # The core Python package for our model and analysis.
│   ├── __init__.py             # Makes the directory a Python package.
│   ├── model.py                # Defines the ODE system and functional responses.
│   ├── equilibria.py           # Functions to find all equilibrium points (E0, E1, E2, E3).
│   ├── stability.py            # Functions for stability analysis (Jacobian, eigenvalues).
│   ├── simulation.py           # Wrapper for running time-course simulations.
│   └── visualization.py        # Reusable plotting functions.
│
├── config.py                   # Central configuration for model parameters and settings.
├── requirements.txt            # Lists project dependencies (numpy, scipy, matplotlib).
├── README.md                   # Project description, setup instructions, and usage guide.
└── .gitignore                  # Specifies files and folders to ignore in version control.
```