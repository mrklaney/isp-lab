from dataclasses import dataclass
from typing import List
import numpy as np
from scipy.linalg import expm


@dataclass
class StochasticProcess:
    states: List[str]
    transitions: List[np.ndarray]  # transitions[i]: T from times[i] to times[i+1]
    times: List[float]

    def __post_init__(self):
        n = len(self.states)
        assert len(self.transitions) == len(self.times) - 1, \
            f"Need {len(self.times)-1} transition matrices for {len(self.times)} time points"
        for i, T in enumerate(self.transitions):
            assert T.shape == (n, n), \
                f"transitions[{i}] must be {n}x{n}, got {T.shape}"

    def evolve(self, p0: np.ndarray) -> List[np.ndarray]:
        """Evolve initial distribution p0 through all time steps."""
        distributions = [p0.copy()]
        p = p0.copy()
        for T in self.transitions:
            p = T @ p
            distributions.append(p.copy())
        return distributions

    def transition_from_to(self, i: int, j: int) -> np.ndarray:
        """Composite transition matrix from times[i] to times[j] (inclusive indices)."""
        n = len(self.states)
        T = np.eye(n)
        for k in range(i, j):
            T = self.transitions[k] @ T
        return T


def make_markov_chain(n_states: int, generator: np.ndarray,
                      times: List[float]) -> StochasticProcess:
    """
    Create a continuous-time Markov chain from a generator matrix L.
    T(t2, t1) = expm(L * (t2 - t1))
    Generator convention: columns of L sum to 0, off-diagonals non-negative.
    """
    states = [str(i) for i in range(n_states)]
    transitions = []
    for i in range(len(times) - 1):
        dt = times[i + 1] - times[i]
        T = expm(generator * dt)
        transitions.append(T)
    return StochasticProcess(states=states, transitions=transitions, times=list(times))
