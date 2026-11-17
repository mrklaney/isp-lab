"""
Matter-wave gratings as an ISP: Raman-Nath diffraction, the Talbot effect and records (notebook 16).

One period of a standing-wave grating, sampled at M points x_j = 2 pi j / M. Momenta are the integers mod M (units of
2 hbar k_L, the grating wavenumber 2 k_L set to 1, with hbar = m = 1). The model is exact on this ring: no truncation.

- A thin grating (Raman-Nath: the atom does not move during the pulse) is exp(-i kappa cos x), diagonal in position.
  In the momentum basis Gamma_pq = J_{p-q}(kappa)^2.
- Free flight is exp(-i p^2 t / 2), diagonal in momentum. The Talbot time is 4 pi.
- Matrices returned by `grating` and `flight` act in the momentum basis.
"""

from typing import Tuple

import numpy as np
from scipy.special import jv

TALBOT = 4 * np.pi
KAPPA_WALL = 2.404825557695773 / 2          # first zero of J0, halved


def grid(M: int) -> Tuple[np.ndarray, np.ndarray, np.ndarray]:
    """Positions x, integer momenta p (FFT order: 0, 1, ..., -1) and the unitary DFT F (position -> momentum)."""
    x = 2 * np.pi * np.arange(M) / M
    p = np.fft.fftfreq(M, 1 / M).astype(int)
    F = np.fft.fft(np.eye(M), norm="ortho")
    return x, p, F


def grating(kappa: float, M: int) -> np.ndarray:
    x, _, F = grid(M)
    return F @ np.diag(np.exp(-1j * kappa * np.cos(x))) @ F.conj().T


def flight(t: float, M: int) -> np.ndarray:
    _, p, _ = grid(M)
    return np.diag(np.exp(-1j * p ** 2 * t / 2))


def gamma(U: np.ndarray) -> np.ndarray:
    return np.abs(U) ** 2


def char_fn(kappa: float, theta: np.ndarray) -> np.ndarray:
    """sum_n J_n(kappa)^2 e^{i n theta} = J0(2 kappa sin(theta / 2)) (Graf's addition theorem)."""
    return jv(0, 2 * kappa * np.sin(theta / 2))


def divisor_kernel(k1: float, k2: float, M: int = 512) -> np.ndarray:
    """The only translation-invariant kernel q with Gamma(k1 + k2) = q * Gamma(k1), in FFT order (q[n] for jump n).
    The family is divisible from k1 to k1 + k2 iff q >= 0."""
    theta = 2 * np.pi * np.arange(M) / M
    return np.real(np.fft.ifft(char_fn(k1 + k2, theta) / char_fn(k1, theta)))


def negative_mass(k1: float, k2: float, M: int = 512) -> float:
    q = divisor_kernel(k1, k2, M)
    return float(-q[q < 0].sum())


def far_weights(k1: float, k2: float, ns, b_frac: float = 0.85, M: int = 8192) -> np.ndarray:
    """Divisor weights q_n on the infinite lattice, accurate far below double precision (k1 below the wall).

    q_hat is analytic for |Im theta| < y1 = 2 arccosh(j01 / (2 k1)) (its nearest poles are at theta = pi +- i y1), so the
    Fourier integral can be moved to Im theta = -b, b = b_frac * y1: q_n = e^{-n b} * (1/2pi) int q_hat(theta - i b)
    e^{-i n theta} dtheta. The shifted coefficients are large enough to read the sign of q_n even when |q_n| ~ 1e-30.
    """
    j01 = 2 * KAPPA_WALL
    if k1 >= KAPPA_WALL:
        raise ValueError("far_weights needs k1 below the wall (1.2024)")
    b = b_frac * 2 * np.arccosh(j01 / (2 * k1))
    z = 2 * np.pi * np.arange(M) / M - 1j * b
    qh = jv(0, 2 * (k1 + k2) * np.sin(z / 2)) / jv(0, 2 * k1 * np.sin(z / 2))
    F = np.fft.fft(qh) / M
    ns = np.asarray(list(ns))
    return np.real(F[ns]) * np.exp(-ns * b)


def record(rho: np.ndarray, eps: float, basis: str = "momentum", ell: float = 1.0) -> np.ndarray:
    """A weak record of strength eps on a momentum-basis density matrix.

    basis="momentum": every coherence between momenta is multiplied by 1 - eps.
    basis="position": the coherence between positions x and y is multiplied by 1 - eps (1 - w(x - y)), with w a Gaussian
    of width ell wrapped round the ring (w(0) = 1): a record that resolves position to about ell (ell > 0). Wrapping keeps
    w positive definite, so the record is a mixture of momentum kicks and a valid quantum channel.
    """
    M = rho.shape[0]
    if basis == "momentum":
        out = rho * (1 - eps)
        out[np.diag_indices(M)] = np.diag(rho)
        return out
    x, _, F = grid(M)
    d = x[:, None] - x[None, :]
    images = 2 * np.pi * np.arange(-20, 21)
    keep = np.exp(-(d[..., None] + images) ** 2 / (2 * ell ** 2)).sum(-1) / np.exp(-images ** 2 / (2 * ell ** 2)).sum()
    rx = F.conj().T @ rho @ F
    rx = rx * (1 - eps * (1 - keep))
    return F @ rx @ F.conj().T


def two_gratings(k1: float, k2: float, t: float, M: int = 64, eps: float = 0.0, basis: str = "momentum",
                 ell: float = 1.0) -> np.ndarray:
    """Momentum distribution after grating k1, flight t (with a record of strength eps halfway), grating k2,
    starting at p = 0."""
    rho = np.zeros((M, M), dtype=complex)
    rho[0, 0] = 1
    half = flight(t / 2, M)
    for U in (grating(k1, M), half):
        rho = U @ rho @ U.conj().T
    rho = record(rho, eps, basis, ell)
    for U in (half, grating(k2, M)):
        rho = U @ rho @ U.conj().T
    return np.real(np.diag(rho))
