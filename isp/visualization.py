from typing import Optional
import numpy as np
import matplotlib.pyplot as plt
from .stochastic import StochasticProcess


def plot_probability_evolution(
    process: StochasticProcess,
    p0: np.ndarray,
    title: str = "Probability Evolution",
    ax: Optional[plt.Axes] = None,
) -> plt.Figure:
    """Plot each state's probability over time."""
    distributions = process.evolve(p0)
    times = process.times
    probs = np.array(distributions)  # shape: (n_times, n_states)

    if ax is None:
        fig, ax = plt.subplots(figsize=(8, 4))
    else:
        fig = ax.figure

    for i, state in enumerate(process.states):
        ax.plot(times, probs[:, i], marker="o", label=f"State {state}")

    ax.set_xlabel("Time")
    ax.set_ylabel("Probability")
    ax.set_title(title)
    ax.legend()
    ax.set_ylim(-0.05, 1.05)
    return fig


def plot_transition_matrix(
    T: np.ndarray,
    title: str = "Transition Matrix",
    ax: Optional[plt.Axes] = None,
) -> plt.Figure:
    """
    Plot a transition matrix as a heatmap.
    Negative entries appear in red — a visual signal of indivisibility.
    """
    if ax is None:
        fig, ax = plt.subplots(figsize=(4, 4))
    else:
        fig = ax.figure

    vmax = max(abs(T.max()), abs(T.min()), 1e-9)
    im = ax.imshow(T, cmap="RdBu", vmin=-vmax, vmax=vmax)
    plt.colorbar(im, ax=ax)

    n = T.shape[0]
    for i in range(n):
        for j in range(n):
            ax.text(j, i, f"{T[i, j]:.3f}", ha="center", va="center", fontsize=8)

    ax.set_title(title)
    ax.set_xlabel("From state")
    ax.set_ylabel("To state")
    return fig
