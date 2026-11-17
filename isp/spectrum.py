# spectrum.py
"""
Energy quantization read off the transition matrices Gamma(t <- 0) = |U(t)|^2. Used by notebook 18.

Two models:
- the s-wave (l = 0) radial hydrogen atom on a grid r_i = i*h (i = 1..N), u(0) = u(R) = 0, atomic units
  (energies in hartree, -1/2n^2 in the continuum limit). Configurations are the grid points ("the electron is at radius r_i").
  Z = 0 gives the same box with no Coulomb attraction: no bound states, only the box's discretised continuum.
- a ring of N sites with a twist alpha (flux 2*pi*alpha threading the ring), used for Wallstrom's objection.

For a real symmetric H with eigenpairs (E_n, v_n), Gamma_jk(t) = |sum_n a_n e^{-iE_n t}|^2 with a_n = v_jn v_kn, so
Gamma_jk(t) = sum_n a_n^2 + sum_{n<m} 2 a_n a_m cos((E_n - E_m) t): its frequencies are energy differences only.
"""

from dataclasses import dataclass, field
import numpy as np


def radial_hydrogen_hamiltonian(h: float, R: float, Z: float = 1.0):
    """H = -1/2 d^2/dr^2 - Z/r on r_i = i*h, i = 1..N with N = R/h - 1 (Dirichlet walls at 0 and R). Returns (H, r)."""
    N = int(round(R / h)) - 1
    r = h * np.arange(1, N + 1)
    off = -0.5 / h ** 2 * np.ones(N - 1)
    H = np.diag(1.0 / h ** 2 - Z / r) + np.diag(off, 1) + np.diag(off, -1)
    return H, r


def ring_hamiltonian(N: int, alpha: float = 0.0, J: float = 1.0) -> np.ndarray:
    """Nearest-neighbour ring, H_{j+1,j} = -J e^{2 pi i alpha / N}: total flux 2*pi*alpha. Energies -2J cos(2pi(m+alpha)/N)."""
    H = np.zeros((N, N), dtype=complex)
    ph = np.exp(2j * np.pi * alpha / N)
    for j in range(N):
        H[(j + 1) % N, j] = -J * ph
        H[j, (j + 1) % N] = -J * np.conj(ph)
    return H


@dataclass
class SpectralModel:
    """A Hamiltonian with cached eigendecomposition; transition matrices are |U(t)|^2."""
    H: np.ndarray
    E: np.ndarray = field(init=False, repr=False)
    V: np.ndarray = field(init=False, repr=False)

    def __post_init__(self):
        self.E, self.V = np.linalg.eigh(self.H)

    @property
    def n(self) -> int:
        return len(self.E)

    def unitary(self, t: float) -> np.ndarray:
        return (self.V * np.exp(-1j * self.E * t)) @ self.V.conj().T

    def gamma(self, t: float) -> np.ndarray:
        """Gamma(t <- 0), columns = starting configuration."""
        return np.abs(self.unitary(t)) ** 2

    def columns(self, j: int, ts) -> np.ndarray:
        """Gamma_{ij}(t) for all i and every t in ts: array (N, len(ts))."""
        ts = np.asarray(ts, dtype=float)
        a = self.V.conj()[j, :]                        # <v_n|j>
        amp = self.V @ (a[:, None] * np.exp(-1j * np.outer(self.E, ts)))
        return np.abs(amp) ** 2

    def entry(self, i: int, j: int, ts) -> np.ndarray:
        """Gamma_{ij}(t) for every t in ts."""
        ts = np.asarray(ts, dtype=float)
        a = self.V[i, :] * self.V.conj()[j, :]
        return np.abs(np.exp(-1j * np.outer(ts, self.E)) @ a) ** 2

    def weights(self, i: int, j: int) -> np.ndarray:
        """|a_n|^2 style weights: a_n = <i|v_n><v_n|j>."""
        return self.V[i, :] * self.V.conj()[j, :]

    def lines(self, i: int, j: int):
        """Spectral lines of Gamma_ij(t): (frequencies |E_n - E_m|, amplitudes 2|a_n a_m|) for n < m, and the constant term.
        For real H the line is 2 a_n a_m cos((E_n - E_m) t), so the signed amplitude is 2 a_n a_m."""
        a = self.weights(i, j)
        nn, mm = np.triu_indices(self.n, 1)
        freq = np.abs(self.E[nn] - self.E[mm])
        w = 2 * np.abs(a[nn] * a[mm])
        return freq, w, float(np.sum(np.abs(a) ** 2))

    def time_average(self, i: int, j: int, mask=None) -> float:
        """Infinite-time average of Gamma_ij for a nondegenerate spectrum: sum_n |a_n|^2 (restricted to `mask` if given)."""
        a2 = np.abs(self.weights(i, j)) ** 2
        return float(a2.sum() if mask is None else a2[mask].sum())

    def time_variance(self, i: int, j: int, mask=None, tol: float = 1e-9) -> float:
        """Infinite-time variance of Gamma_ij, sum over distinct gaps w > 0 of 2 |c_w|^2 with c_w = sum a_n conj(a_m) over pairs
        E_m - E_n = w (within tol). Pairs sharing a gap are grouped, so degenerate gaps (e.g. the symmetric Z = 0 box) are
        handled; when all gaps are distinct it reduces to sum_{n != m} |a_n|^2 |a_m|^2. With `mask`, only levels in the mask."""
        a = self.weights(i, j)
        E = self.E
        if mask is not None:
            a, E = a[mask], E[mask]
        nn, mm = np.triu_indices(len(E), 1)                 # E sorted ascending, so E[mm] >= E[nn]
        w = E[mm] - E[nn]
        c = a[nn] * np.conj(a[mm])
        keep = w > tol
        w, c = w[keep], c[keep]
        if len(w) == 0:
            return 0.0
        order = np.argsort(w)
        w, c = w[order], c[order]
        group = np.concatenate([[0], np.cumsum(np.diff(w) > tol * np.maximum(1.0, w[1:]))])
        sums = np.zeros(group[-1] + 1, dtype=complex)
        np.add.at(sums, group, c)
        return float(2 * np.sum(np.abs(sums) ** 2))


def distinguishability(col_j: np.ndarray, col_k: np.ndarray) -> np.ndarray:
    """Kolmogorov distance 1/2 sum_i |Gamma_ij - Gamma_ik| between two columns (shape (N,) or (N, T))."""
    return 0.5 * np.abs(col_j - col_k).sum(axis=0)


def revival(D: np.ndarray) -> float:
    """max over t > t' of D(t) - D(t'): zero for every divisible process (stochastic maps never increase D)."""
    D = np.asarray(D, dtype=float)
    return float(np.max(D - np.minimum.accumulate(D)))


def record_chain(G_tau: np.ndarray, n: int) -> np.ndarray:
    """Barandes's Markov chain with a division event every tau: Gamma(tau)^n."""
    return np.linalg.matrix_power(G_tau, n)


def is_permutation(G: np.ndarray, tol: float = 1e-9) -> bool:
    return bool(np.all((G < tol) | (G > 1 - tol)) and np.allclose(G.sum(0), 1) and np.allclose(G.sum(1), 1))
