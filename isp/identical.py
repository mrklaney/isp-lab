"""
Identical particles as an indivisible stochastic process (notebook 14).

n free particles on N sites, all moved by the same single-particle unitary U. Configurations are occupation tuples
(m_0, ..., m_{N-1}) with sum n: what a detector that cannot tell the particles apart records.
- bosons:          Gamma(m <- k) = |perm U[m, k]|^2 / (prod m! prod k!)
- fermions:        Gamma(m <- k) = |det U[m, k]|^2              (occupations 0 or 1 only)
- distinguishable: Gamma(m <- k) = perm(|U[m, k]|^2) / prod m!  (independent walkers, labels forgotten)
U[m, k] is the n x n submatrix with rows = sites of m and columns = sites of k, each repeated by its occupation.

Under division events every tau (records of the occupations), Gamma(tau)^(s/tau^2) -> exp(s L) as tau -> 0, where L
is the classical generator with hopping rates |h_ji|^2 times
- bosons:          m_i (m_j + 1)   (the symmetric inclusion process)
- fermions:        m_i (1 - m_j)   (the symmetric exclusion process)
- distinguishable: m_i             (independent random walkers)
"""

import itertools
import math
from typing import List, Tuple

import numpy as np

KINDS = ("boson", "fermion", "distinguishable")


def configurations(N: int, n: int, kind: str) -> List[Tuple[int, ...]]:
    """Occupation tuples of n particles on N sites; fermions allow at most one per site."""
    if kind == "fermion":
        return [tuple(1 if i in c else 0 for i in range(N)) for c in itertools.combinations(range(N), n)]
    return [tuple(c.count(i) for i in range(N)) for c in itertools.combinations_with_replacement(range(N), n)]


def _sites(m) -> List[int]:
    return [i for i, k in enumerate(m) for _ in range(k)]


def permanent(A: np.ndarray) -> complex:
    n = A.shape[0]
    return sum(np.prod([A[i, s[i]] for i in range(n)]) for s in itertools.permutations(range(n))) if n else 1.0


def gamma(U: np.ndarray, n: int, kind: str) -> Tuple[np.ndarray, List[Tuple[int, ...]]]:
    """Column-stochastic Gamma on occupation configurations, and the configuration list (row/column order)."""
    if kind not in KINDS:
        raise ValueError(f"kind must be one of {KINDS}")
    C = configurations(U.shape[0], n, kind)
    G = np.zeros((len(C), len(C)))
    for b, k in enumerate(C):
        cols = _sites(k)
        for a, m in enumerate(C):
            sub = U[np.ix_(_sites(m), cols)]
            fm = np.prod([math.factorial(x) for x in m])
            if kind == "fermion":
                G[a, b] = abs(np.linalg.det(sub)) ** 2
            elif kind == "boson":
                G[a, b] = abs(permanent(sub)) ** 2 / (fm * np.prod([math.factorial(x) for x in k]))
            else:
                G[a, b] = permanent(np.abs(sub) ** 2).real / fm
    return G, C


def classical_generator(h: np.ndarray, n: int, kind: str) -> Tuple[np.ndarray, List[Tuple[int, ...]]]:
    """The Markov generator that dense division events produce (see module docstring)."""
    N = h.shape[0]
    C = configurations(N, n, kind)
    idx = {c: a for a, c in enumerate(C)}
    L = np.zeros((len(C), len(C)))
    for b, m in enumerate(C):
        for i in range(N):
            for j in range(N):
                if i == j or h[j, i] == 0 or m[i] == 0:
                    continue
                if kind == "fermion" and m[j] == 1:
                    continue
                new = list(m); new[i] -= 1; new[j] += 1
                factor = m[i] * (m[j] + 1) if kind == "boson" else m[i]
                L[idx[tuple(new)], b] += abs(h[j, i]) ** 2 * factor
        L[b, b] = -L[:, b].sum()
    return L, C


def stationary(L: np.ndarray) -> np.ndarray:
    w, v = np.linalg.eig(L)
    p = np.real(v[:, np.argmin(np.abs(w))])
    return p / p.sum()


def chain(N: int, J: float = 1.0, ring: bool = False) -> np.ndarray:
    """Single-particle nearest-neighbour hopping matrix (-J on each bond)."""
    h = np.zeros((N, N))
    for i in range(N - 1):
        h[i, i + 1] = h[i + 1, i] = -J
    if ring:
        h[0, N - 1] = h[N - 1, 0] = -J
    return h


def embed(G_small: np.ndarray, C_small, C_big) -> np.ndarray:
    """Place a Gamma on a subset of configurations (e.g. fermions) into the bigger configuration list, zeros elsewhere."""
    G = np.zeros((len(C_big), len(C_big)))
    pos = [C_big.index(c) for c in C_small]
    G[np.ix_(pos, pos)] = G_small
    return G
