# double_slit.py
#
# A double slit built as a genuine indivisible stochastic process, so that
# interference and indivisibility can be measured on the *same* object.
#
# Three times, one particle, n transverse modes:
#
#     t0  source mode          --U1-->  t1  slit plane  --U2-->  t2  screen
#
# U2 is the unitary DFT: Fraunhofer (far-field) propagation. This is the
# physically correct slit-to-screen propagator, and being unitary it makes the
# two slit amplitudes *orthonormal* — which is what keeps the Born-rule
# probabilities normalised without any hand-applied rescaling.
#
# The associated stochastic process is unistochastic, Gamma[i,j] = |U[i,j]|^2,
# and the three matrices it needs are
#
#     Gamma(t1,t0) = |U1|^2
#     Gamma(t2,t1) = |U2|^2
#     Gamma(t2,t0) = |U2 U1|^2      (coherent)   vs  |U2|^2 |U1|^2  (decohered)
#
# Divisibility asks whether the last one factors through the middle one. It does
# not, and the amount by which it fails, read off the source column, *is* the
# interference pattern.

from typing import Any, Dict, List
import numpy as np

from .stochastic import PairwiseProcess


def far_field_propagator(n_modes: int) -> np.ndarray:
    """
    Unitary DFT: the Fraunhofer propagator from the slit plane to the screen.

    Column m is the amplitude reaching each screen pixel from slit m. Columns are
    orthonormal because the matrix is unitary, so distinct slits contribute
    non-overlapping amplitudes and probabilities normalise on their own.
    """
    k = np.arange(n_modes)
    return np.exp(2j * np.pi * np.outer(k, k) / n_modes) / np.sqrt(n_modes)


def slit_preparation(n_modes: int, slit_a: int, slit_b: int,
                     source: int = 0, seed: int = 7) -> np.ndarray:
    """
    A unitary whose `source` column is the balanced superposition
    (|slit_a> + |slit_b>) / sqrt(2).

    Only that one column carries physical content — it is what a particle
    emitted from the source actually does. The remaining columns are an
    arbitrary orthonormal completion, required because a process needs a full
    transition matrix. Every prediction in the notebook depends only on the
    source column and is therefore independent of `seed`; the notebook checks
    this explicitly.
    """
    v = np.zeros(n_modes, dtype=complex)
    v[slit_a] = v[slit_b] = 1 / np.sqrt(2)

    rng = np.random.default_rng(seed)
    M = rng.normal(size=(n_modes, n_modes)) + 1j * rng.normal(size=(n_modes, n_modes))
    M[:, source] = v
    Q, R = np.linalg.qr(M)
    return Q * np.exp(-1j * np.angle(np.diag(R)))  # fix phases so Q[:, source] == v


def double_slit_matrices(n_modes: int = 24, slit_a: int = 10, slit_b: int = 13,
                         coherence: float = 1.0, source: int = 0,
                         seed: int = 7) -> Dict[str, Any]:
    """
    Build the three transition matrices of the double-slit process.

    `coherence` c in [0, 1] is the surviving off-diagonal coherence between the
    two slit amplitudes — c = 1 is a fully coherent particle, c = 0 is a
    which-path measurement at the slits. Dephasing the slit-plane density matrix
    by c, rho[m,n] -> rho[m,n] * (delta[m,n] + c*(1 - delta[m,n])), and
    propagating gives, for every input mode j,

        Gamma_c(t2,t0)[k,j] = (1-c) * (|U2|^2 |U1|^2)[k,j] + c * |U2 U1|^2[k,j]

    so the family interpolates linearly between the decohered and coherent
    processes. That is derived, not posited.

    Returns a dict with keys U1, U2, gamma_10, gamma_21, gamma_20,
    gamma_20_coherent, gamma_20_decohered, and the index metadata.
    """
    if not 0.0 <= coherence <= 1.0:
        raise ValueError(f"coherence must be in [0, 1], got {coherence}")

    U1 = slit_preparation(n_modes, slit_a, slit_b, source=source, seed=seed)
    U2 = far_field_propagator(n_modes)

    gamma_10 = np.abs(U1) ** 2
    gamma_21 = np.abs(U2) ** 2
    gamma_20_coherent = np.abs(U2 @ U1) ** 2
    gamma_20_decohered = gamma_21 @ gamma_10
    gamma_20 = (1 - coherence) * gamma_20_decohered + coherence * gamma_20_coherent

    return {
        "U1": U1,
        "U2": U2,
        "gamma_10": gamma_10,
        "gamma_21": gamma_21,
        "gamma_20": gamma_20,
        "gamma_20_coherent": gamma_20_coherent,
        "gamma_20_decohered": gamma_20_decohered,
        "n_modes": n_modes,
        "slit_a": slit_a,
        "slit_b": slit_b,
        "source": source,
        "coherence": coherence,
    }


def make_double_slit_process(n_modes: int = 24, slit_a: int = 10, slit_b: int = 13,
                             coherence: float = 1.0, source: int = 0,
                             seed: int = 7,
                             times: List[float] = None) -> PairwiseProcess:
    """
    The double slit as a PairwiseProcess, ready for check_divisibility_lp().

    Divisible exactly when coherence == 0.
    """
    if times is None:
        times = [0.0, 1.0, 2.0]

    m = double_slit_matrices(n_modes, slit_a, slit_b, coherence, source, seed)
    return PairwiseProcess(
        states=[str(i) for i in range(n_modes)],
        times=list(times),
        matrices={
            (0, 1): m["gamma_10"],
            (1, 2): m["gamma_21"],
            (0, 2): m["gamma_20"],
        },
    )


def screen_distribution(matrices: Dict[str, Any], which: str = "gamma_20") -> np.ndarray:
    """Probability over screen pixels for a particle emitted from the source."""
    return matrices[which][:, matrices["source"]]


def fringe_visibility(p: np.ndarray) -> float:
    """Michelson visibility (max - min) / (max + min) of a screen distribution."""
    hi, lo = p.max(), p.min()
    return float((hi - lo) / (hi + lo)) if hi + lo > 0 else 0.0
