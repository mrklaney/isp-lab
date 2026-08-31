from dataclasses import dataclass
from typing import Dict, List, Tuple
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


@dataclass
class PairwiseProcess:
    """
    A process specified by its family of transition matrices {Gamma(t_j, t_i)}
    directly, rather than by incremental steps that are chained together.

    StochasticProcess stores increments and *derives* T(i→k) as a product, which
    quietly assumes an increment exists. For an indivisible process it may not:
    if Gamma(t_j, t_i) is singular there can be no matrix at all — signed or
    otherwise — that composes to give Gamma(t_k, t_i). The balanced double slit
    is exactly this case (see isp.double_slit), so it cannot be expressed as a
    StochasticProcess without changing the physics.

    Barandes' definition of a process is this family of matrices; divisibility is
    then a *question* about the family, not something baked into its storage.

    matrices maps (i, j) with i < j to Gamma(t_j, t_i).
    """
    states: List[str]
    times: List[float]
    matrices: Dict[Tuple[int, int], np.ndarray]

    def __post_init__(self):
        n = len(self.states)
        for (i, j), M in self.matrices.items():
            assert 0 <= i < j < len(self.times), f"bad index pair {(i, j)}"
            assert M.shape == (n, n), f"matrices[{(i, j)}] must be {n}x{n}, got {M.shape}"
            assert np.allclose(M.sum(axis=0), 1.0), \
                f"matrices[{(i, j)}] columns must sum to 1"
            assert np.all(M >= -1e-12), f"matrices[{(i, j)}] must be non-negative"

    def transition_from_to(self, i: int, j: int) -> np.ndarray:
        """Transition matrix from times[i] to times[j]."""
        if i == j:
            return np.eye(len(self.states))
        return self.matrices[(i, j)]

    def distribution_at(self, i: int, p0: np.ndarray) -> np.ndarray:
        """Distribution at times[i] given the distribution at times[0]."""
        return self.transition_from_to(0, i) @ p0


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
