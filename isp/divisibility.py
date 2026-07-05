from typing import Any, Dict
import numpy as np
from .stochastic import StochasticProcess


def check_divisibility(process: StochasticProcess,
                       tol: float = 1e-10) -> Dict[str, Any]:
    """
    Check if a stochastic process is divisible.

    For all index triples i < j < k, tests whether
        T(i→k) = T(j→k) @ T(i→j)
    can be satisfied by a valid stochastic matrix T(j→k).

    Returns a dict with keys:
        divisible     : bool
        failure_mode  : "singular_matrix" | "negative_entries" |
                        "normalization_violated" | None
        at_times      : (times[i], times[j], times[k]) | None
        message       : str | None
    """
    times = process.times
    n_times = len(times)

    for i in range(n_times):
        for j in range(i + 1, n_times):
            for k in range(j + 1, n_times):
                T_ik = process.transition_from_to(i, k)  # t_i → t_k
                T_ij = process.transition_from_to(i, j)  # t_i → t_j

                det_val = np.linalg.det(T_ij)
                if abs(det_val) < tol:
                    return {
                        "divisible": False,
                        "failure_mode": "singular_matrix",
                        "at_times": (times[i], times[j], times[k]),
                        "message": (
                            f"T({times[i]},{times[j]}) is singular — "
                            f"det={det_val:.2e}"
                        ),
                    }

                T_jk_candidate = T_ik @ np.linalg.inv(T_ij)

                if np.any(T_jk_candidate < -tol):
                    return {
                        "divisible": False,
                        "failure_mode": "negative_entries",
                        "at_times": (times[i], times[j], times[k]),
                        "message": (
                            f"Intermediate matrix T({times[k]},{times[j]}) "
                            f"has negative entries: min={T_jk_candidate.min():.6f}"
                        ),
                    }

                col_sums = T_jk_candidate.sum(axis=0)
                if not np.allclose(col_sums, 1.0, atol=tol):
                    return {
                        "divisible": False,
                        "failure_mode": "normalization_violated",
                        "at_times": (times[i], times[j], times[k]),
                        "message": (
                            f"Intermediate matrix columns don't sum to 1: {col_sums}"
                        ),
                    }

    return {"divisible": True, "failure_mode": None, "at_times": None, "message": None}


def indivisibility_signature(process: StochasticProcess,
                              tol: float = 1e-10) -> float:
    """
    Scalar measure of indivisibility.
    Returns 0.0 for divisible (classical) processes.
    Returns > 0.0 for indivisible processes (magnitude of most negative entry
    found across all candidate intermediate matrices).
    """
    times = process.times
    n_times = len(times)
    max_negativity = 0.0

    for i in range(n_times):
        for j in range(i + 1, n_times):
            for k in range(j + 1, n_times):
                T_ik = process.transition_from_to(i, k)
                T_ij = process.transition_from_to(i, j)

                if abs(np.linalg.det(T_ij)) < tol:
                    continue

                T_jk_candidate = T_ik @ np.linalg.inv(T_ij)
                negativity = max(0.0, -T_jk_candidate.min())
                max_negativity = max(max_negativity, negativity)

    return max_negativity
