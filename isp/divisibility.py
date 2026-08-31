from typing import Any, Dict, Optional, Tuple
import numpy as np
import scipy.sparse as sp
from scipy.optimize import linprog

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


# ---------------------------------------------------------------------------
# Inverse-free divisibility test
#
# check_divisibility() above solves T(j→k) = T(i→k) @ inv(T(i→j)), so it needs
# T(i→j) to be invertible. Many physically natural processes make that
# impossible — the balanced double slit of notebook 05 is the clean example:
# if a unitary sends the source to (|A> + |B>)/sqrt(2), unitarity saturates
# Cauchy-Schwarz and *forces* rows A and B of |U|^2 to be equal, so |U|^2 is
# rank-deficient for every such model. The inverse-based test is then not
# merely inconclusive, it is structurally unavailable.
#
# The functions below test Barandes' condition as originally stated — does
# *any* valid stochastic intermediate matrix exist — as a linear program.
# No inverse, so singularity is irrelevant, and the answer is exact rather
# than "inconclusive".
# ---------------------------------------------------------------------------


def _intermediate_lp(T_ik: np.ndarray, T_ij: np.ndarray,
                     minimize_residual: bool) -> Tuple[bool, float, Optional[np.ndarray]]:
    """
    Search for a stochastic matrix M with  M @ T_ij == T_ik.

    Constraints: M >= 0 elementwise, columns of M sum to 1.
    Vectorising row-major, M @ T_ij becomes (I ⊗ T_ij.T) @ vec(M).

    minimize_residual=False : pure feasibility.
    minimize_residual=True  : minimise the L1 residual ||M @ T_ij - T_ik||_1
                              via +/- slack variables, which is always
                              feasible and returns 0 exactly when divisible.

    Returns (feasible, residual, M).
    """
    n = T_ij.shape[0]
    nv = n * n

    compose = sp.kron(sp.identity(n, format="csr"), sp.csr_matrix(T_ij.T))
    colsums = sp.kron(sp.csr_matrix(np.ones((1, n))), sp.identity(n, format="csr"))

    if minimize_residual:
        # variables: [vec(M) | s_plus | s_minus]
        A_eq = sp.bmat([
            [compose, -sp.identity(nv, format="csr"), sp.identity(nv, format="csr")],
            [colsums, None, None],
        ], format="csr")
        b_eq = np.concatenate([T_ik.ravel(), np.ones(n)])
        cost = np.concatenate([np.zeros(nv), np.ones(2 * nv)])
        n_total = 3 * nv
    else:
        A_eq = sp.vstack([compose, colsums], format="csr")
        b_eq = np.concatenate([T_ik.ravel(), np.ones(n)])
        cost = np.zeros(nv)
        n_total = nv

    res = linprog(cost, A_eq=A_eq, b_eq=b_eq,
                  bounds=[(0, None)] * n_total, method="highs")

    if not res.success:
        return False, float("inf"), None

    M = res.x[:nv].reshape(n, n)
    residual = float(res.fun) if minimize_residual else 0.0
    return True, residual, M


def divisibility_defect(process: StochasticProcess,
                        tol: float = 1e-8) -> float:
    """
    Inverse-free scalar measure of indivisibility.

    For every triple i < j < k, computes the smallest achievable L1 residual

        min  || M @ T(i→j) - T(i→k) ||_1     over  M >= 0, columns summing to 1

    and returns the largest such residual. Exactly 0.0 for a divisible process
    (a valid intermediate matrix exists); strictly positive otherwise, growing
    with how far the process sits from the divisible set.

    Unlike indivisibility_signature(), this never needs T(i→j) to be invertible
    and never silently skips a triple.
    """
    times = process.times
    n_times = len(times)
    worst = 0.0

    for i in range(n_times):
        for j in range(i + 1, n_times):
            for k in range(j + 1, n_times):
                T_ik = process.transition_from_to(i, k)
                T_ij = process.transition_from_to(i, j)
                _, residual, _ = _intermediate_lp(T_ik, T_ij, minimize_residual=True)
                if residual > worst:
                    worst = residual

    return 0.0 if worst < tol else worst


def check_divisibility_lp(process: StochasticProcess,
                          tol: float = 1e-8) -> Dict[str, Any]:
    """
    Divisibility test stated the way Barandes states it: is there *any* valid
    stochastic intermediate matrix T(j→k) satisfying T(i→k) = T(j→k) @ T(i→j)?

    Solved as a linear program, so it works on singular T(i→j) where
    check_divisibility() can only report "singular_matrix".

    Returns a dict with keys:
        divisible     : bool
        failure_mode  : "no_valid_intermediate_matrix" | None
        at_times      : (times[i], times[j], times[k]) | None
        defect        : float — 0.0 if divisible, else the L1 residual
        witness       : np.ndarray | None — a valid T(j→k) when divisible,
                        for the *last* triple checked
        message       : str | None
    """
    times = process.times
    n_times = len(times)
    witness = None

    for i in range(n_times):
        for j in range(i + 1, n_times):
            for k in range(j + 1, n_times):
                T_ik = process.transition_from_to(i, k)
                T_ij = process.transition_from_to(i, j)

                feasible, _, M = _intermediate_lp(T_ik, T_ij, minimize_residual=False)
                if feasible:
                    witness = M
                    continue

                _, defect, _ = _intermediate_lp(T_ik, T_ij, minimize_residual=True)
                return {
                    "divisible": False,
                    "failure_mode": "no_valid_intermediate_matrix",
                    "at_times": (times[i], times[j], times[k]),
                    "defect": defect,
                    "witness": None,
                    "message": (
                        f"No stochastic T({times[k]},{times[j]}) satisfies "
                        f"T({times[k]},{times[i]}) = T({times[k]},{times[j]}) @ "
                        f"T({times[j]},{times[i]}); L1 defect={defect:.6f}"
                    ),
                }

    return {
        "divisible": True,
        "failure_mode": None,
        "at_times": None,
        "defect": 0.0,
        "witness": witness,
        "message": None,
    }
