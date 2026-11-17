# wick.py
"""
Real time vs imaginary time for the same Hamiltonian on a finite configuration space (notebook 12).

Real time:      Gamma(t) = |exp(-iHt)|^2                               (unistochastic, generally indivisible)
Imaginary time: P(tau)_ij = psi0(i) [exp(-(H - E0) tau)]_ij / psi0(j)  (ground-state transform)

P(tau) is a Markov semigroup (stochastic, P(a + b) = P(b) P(a)) exactly when the ground state psi0 can be chosen
positive and exp(-H tau) has no negative entries, which holds when H is stoquastic (off-diagonal entries <= 0) in some
gauge D H D, D = diag(+-1). Diagonal rephasings leave the real-time Gamma unchanged; that freedom is what the sign
problem is about.
"""

import itertools
from typing import List, Optional, Tuple
import numpy as np
from scipy.linalg import expm


def real_gamma(H: np.ndarray, t: float) -> np.ndarray:
    """Real-time transition matrix |exp(-iHt)|^2."""
    return np.abs(expm(-1j * H * t)) ** 2


def euclidean_markov(H: np.ndarray, tau: float) -> Tuple[np.ndarray, np.ndarray]:
    """
    Ground-state transform of exp(-H tau). Returns (P, psi0) with psi0 the ground state, sign chosen so its largest
    entry is positive. P has columns summing to 1 for any real symmetric H.
    P is unchanged by a +-1 gauge D H D; for a connected lattice with a nondegenerate ground state it is stochastic for
    every tau exactly when some such gauge makes H stoquastic. With a degenerate ground state, psi0 (and P) depends on
    which eigenvector eigh returns.
    """
    w, V = np.linalg.eigh(H)
    psi = V[:, 0].real
    psi = psi * np.sign(psi[np.argmax(np.abs(psi))])
    K = expm(-(H - w[0] * np.eye(len(H))) * tau).real
    return (psi[:, None] * K) / psi[None, :], psi


def negative_mass(D: np.ndarray, tol: float = 1e-12) -> float:
    """Largest total negative weight in any column of D (0 when D has no negative entries)."""
    return float(-np.clip(D, None, 0).sum(axis=0).min()) if np.any(D < -tol) else 0.0


def is_stoquastic(H: np.ndarray, tol: float = 1e-12) -> bool:
    """Real, with every off-diagonal entry <= 0."""
    off = H - np.diag(np.diag(H))
    return bool(np.allclose(np.imag(off), 0, atol=tol) and np.all(np.real(off) <= tol))


def stoquastic_gauge(H: np.ndarray) -> Optional[np.ndarray]:
    """
    Search the 2^(N-1) sign gauges D = diag(1, +-1, ...) for one making D H D stoquastic. Returns D's diagonal, or None.
    Exhaustive, so only for small N.
    """
    N = len(H)
    for s in itertools.product([1, -1], repeat=N - 1):
        d = np.array((1,) + s, dtype=float)
        if is_stoquastic(d[:, None] * H * d[None, :]):
            return d
    return None


def hopping_hamiltonian(N: int, J: float = 1.0, potential=None, ring: bool = False, flux: float = 0.0) -> np.ndarray:
    """One particle on N sites: hopping amplitude -J between neighbours (a ring closes with phase e^{i flux}), plus a potential."""
    H = np.zeros((N, N), dtype=complex)
    for i in range(N - 1):
        H[i, i + 1] = H[i + 1, i] = -J
    if ring:
        H[N - 1, 0] = -J * np.exp(1j * flux)
        H[0, N - 1] = np.conj(H[N - 1, 0])
    if potential is not None:
        H += np.diag(potential)
    return H.real if np.allclose(H.imag, 0) else H


def two_particle_hamiltonian(N: int, ring: bool, fermion: bool, J: float = 1.0,
                             potential=None) -> Tuple[np.ndarray, List[Tuple[int, int]]]:
    """
    Two hard-core particles on N sites; configurations are the occupied pairs (i < j). Hopping -J between neighbours.
    Fermions pick up (-1)^(number of particles strictly between the two sites in site order) when hopping: the
    Jordan-Wigner sign. On an open chain with nearest-neighbour hopping no particle is ever in between, so fermions and
    hard-core bosons have the same H. A hop across a ring's closing bond passes the other particle.
    """
    confs = list(itertools.combinations(range(N), 2))
    idx = {c: k for k, c in enumerate(confs)}
    H = np.zeros((len(confs), len(confs)))
    bonds = [(i, i + 1) for i in range(N - 1)] + ([(N - 1, 0)] if ring else [])
    for c in confs:
        occ = set(c)
        for a, b in bonds:
            for src, dst in ((a, b), (b, a)):
                if src in occ and dst not in occ:
                    new = tuple(sorted((occ - {src}) | {dst}))
                    sign = 1.0
                    if fermion:
                        lo, hi = min(src, dst), max(src, dst)
                        sign = (-1.0) ** sum(1 for x in occ if lo < x < hi)
                    H[idx[new], idx[c]] += -J * sign
    if potential is not None:
        v = np.asarray(potential, dtype=float)
        H += np.diag([v[list(c)].sum() for c in confs])
    return H, confs
