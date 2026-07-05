# quantum.py

from typing import List
import numpy as np
from .stochastic import StochasticProcess


def density_matrix_to_stochastic_state(rho: np.ndarray) -> np.ndarray:
    """
    Extract occupation probabilities from a density matrix.
    p[i] = rho[i,i] — the diagonal gives the Born-rule probabilities
    for the computational basis.
    """
    p = np.real(np.diag(rho))
    return np.clip(p, 0, None)


def unitary_to_transition_matrix(U: np.ndarray) -> np.ndarray:
    """
    Convert unitary U to the transition matrix for occupation probabilities.
    T[i,j] = |U[i,j]|^2
    Each column sums to 1 because U is unitary (columns are unit vectors).
    """
    return np.abs(U) ** 2


def make_qubit_sigmax_process(omega: float,
                               times: List[float]) -> StochasticProcess:
    """
    Stochastic process from qubit evolution under H = (omega/2) * sigma_x.

    The absolute transition from time 0 to time t is:
        T(t)[i,j] = |U(t)[i,j]|^2
                  = [[cos²(ω·t/2), sin²(ω·t/2)],
                     [sin²(ω·t/2), cos²(ω·t/2)]]

    Each stored incremental matrix is T(0→t_{i+1}) @ inv(T(0→t_i)), so that
    transition_from_to(0, k) chains to give the absolute evolution T(0→t_k).
    For non-Markovian (quantum) dynamics the incremental matrix may have
    negative entries, which is exactly what check_divisibility detects.
    """
    t0 = times[0]

    def T_abs(t: float) -> np.ndarray:
        """Absolute transition matrix from t0 to t."""
        dt = t - t0
        theta = omega * dt / 2
        c2, s2 = np.cos(theta) ** 2, np.sin(theta) ** 2
        return np.array([[c2, s2], [s2, c2]])

    transitions = []
    T_prev = np.eye(2)
    for i in range(len(times) - 1):
        T_next = T_abs(times[i + 1])
        T_incr = T_next @ np.linalg.inv(T_prev) if i > 0 else T_next
        transitions.append(T_incr)
        T_prev = T_next

    return StochasticProcess(
        states=["0", "1"],
        transitions=transitions,
        times=list(times),
    )


def born_rule(rho: np.ndarray, measurement_operator: np.ndarray) -> float:
    """
    Born rule probability: Tr(M @ rho).
    measurement_operator: a POVM element (positive semidefinite).
    """
    return float(np.real(np.trace(measurement_operator @ rho)))
