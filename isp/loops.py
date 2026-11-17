"""
Loop phases in Gamma: the Aharonov-Bohm ring and Berry's phase (notebook 15).

Ring: N sites, hopping -J e^{i phi_k} from site k to k+1 (mod N). A gauge transformation (diagonal rephasing D H D^dagger)
moves phases between bonds and leaves Gamma = |U|^2 unchanged; only the flux Phi = sum_k phi_k (mod 2 pi) matters.

Berry: spin-1/2 in a field of strength B0 at polar angle theta, rotating once about z in time T. Configurations are the
z-basis states. In the frame rotating with the field the Hamiltonian is constant, so the loop unitary is exact:
U(t) = exp(-i w t sz/2) exp(-i (H0 - w sz/2) t), with w = 2 pi / T.
"""

from typing import Tuple

import numpy as np
from scipy.linalg import expm

SX = np.array([[0, 1], [1, 0]], dtype=complex)
SZ = np.diag([1.0, -1.0]).astype(complex)


def ring_hamiltonian(N: int, flux: float = 0.0, J: float = 1.0, gauge: str = "one-bond") -> np.ndarray:
    """Ring with total flux `flux`, placed on the closing bond ("one-bond") or spread evenly ("uniform")."""
    phases = np.full(N, flux / N) if gauge == "uniform" else np.r_[np.zeros(N - 1), flux]
    H = np.zeros((N, N), dtype=complex)
    for k in range(N):
        H[(k + 1) % N, k] += -J * np.exp(1j * phases[k])
        H[k, (k + 1) % N] += -J * np.exp(-1j * phases[k])
    return H


def gamma(H: np.ndarray, t: float) -> np.ndarray:
    return np.abs(expm(-1j * H * t)) ** 2


def recorded(H: np.ndarray, tau: float, s: float) -> np.ndarray:
    """Gamma with a division event every tau, over a stretch of s / tau^2 steps (the Zeno-scaled time of notebook 11)."""
    return np.linalg.matrix_power(gamma(H, tau), int(round(s / tau ** 2)))


def dephased_populations(H: np.ndarray, tau: float, eps: float, steps: int, start: int = 0) -> np.ndarray:
    """Configuration probabilities after `steps` steps of tau, each followed by a weak record that multiplies every
    coherence between configurations by (1 - eps): eps = 0 is no record, eps = 1 a full division event."""
    N = H.shape[0]
    U = expm(-1j * H * tau)
    rho = np.zeros((N, N), dtype=complex)
    rho[start, start] = 1
    off = ~np.eye(N, dtype=bool)
    for _ in range(steps):
        rho = U @ rho @ U.conj().T
        rho[off] *= 1 - eps
    return np.real(np.diag(rho))


def field_hamiltonian(B0: float, theta: float, phi: float = 0.0) -> np.ndarray:
    """-B0 n.sigma with n at polar angle theta, azimuth phi."""
    R = expm(-1j * phi * SZ / 2)
    return R @ (-B0 * (np.sin(theta) * SX + np.cos(theta) * SZ)) @ R.conj().T


def loop_unitary(B0: float, theta: float, T: float, frac: float = 1.0, direction: int = 1) -> np.ndarray:
    """Exact evolution for a fraction `frac` of one loop of the field about z (direction +1 or -1)."""
    w = direction * 2 * np.pi / T
    t = frac * T
    return expm(-1j * w * t * SZ / 2) @ expm(-1j * (field_hamiltonian(B0, theta) - w * SZ / 2) * t)


def energy_basis(B0: float, theta: float, phi: float = 0.0) -> np.ndarray:
    """Columns: instantaneous eigenvectors (ground state first)."""
    return np.linalg.eigh(field_hamiltonian(B0, theta, phi))[1]


def fringe_phase(x: np.ndarray, P: np.ndarray) -> Tuple[float, float]:
    """Fit P = a0 + A cos(2x - phase); return (phase, A)."""
    M = np.c_[np.ones_like(x), np.cos(2 * x), np.sin(2 * x)]
    _, a, b = np.linalg.lstsq(M, P, rcond=None)[0]
    return float(np.arctan2(b, a)), float(np.hypot(a, b))


def solid_angle(theta: float) -> float:
    """Solid angle swept by a field vector at polar angle theta going once around z."""
    return 2 * np.pi * (1 - np.cos(theta))
