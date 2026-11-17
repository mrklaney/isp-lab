# decay.py
"""
One level |b> coupled to a band of M levels: the textbook model behind Fermi's golden rule.

Configurations are b (index 0) and the band levels k_1..k_M (indices 1..M). The band is equally spaced
(spacing delta, bandwidth W = M*delta) and centred on energy 0; b sits at e0 (0 unless offset). The coupling is the
same g for every band level (a flat band) unless a profile g_k is passed as `couplings` (a structured band).
Gamma(t <- 0) = |U(t)|^2 with U(t) = exp(-iHt). Used by notebooks 10 and 11.
"""

from dataclasses import dataclass, field
from typing import Optional
import numpy as np


def band_energies(M: int, delta: float) -> np.ndarray:
    """Equally spaced band energies centred on 0."""
    return (np.arange(M) - (M - 1) / 2) * delta


def level_band_hamiltonian(M: int, delta: float, g: float, e0: float = 0.0,
                           couplings: Optional[np.ndarray] = None) -> np.ndarray:
    """H with b at index 0 (energy e0), band energies centred on 0, and coupling g_k between b and band level k
    (g for every level unless `couplings` gives the profile)."""
    gk = np.full(M, g, dtype=float) if couplings is None else np.asarray(couplings, dtype=float)
    H = np.zeros((M + 1, M + 1))
    H[0, 0] = e0
    H[1:, 1:] = np.diag(band_energies(M, delta))
    H[0, 1:] = gk
    H[1:, 0] = gk
    return H


def lorentzian_couplings(M: int, delta: float, g0: float, center: float, width: float) -> np.ndarray:
    """Structured band: g_k^2 = g0^2 * width^2 / ((eps_k - center)^2 + width^2), peaked at `center`."""
    eps = band_energies(M, delta)
    return g0 * width / np.sqrt((eps - center) ** 2 + width ** 2)


def golden_rule_rate(delta: float, g: float) -> float:
    """Fermi's golden rule for a flat band: 2*pi*g^2 * (density of states 1/delta)."""
    return 2 * np.pi * g ** 2 / delta


def agility_squared(H: np.ndarray, j: int = 0) -> float:
    """nu^2 = -1/2 d^2/dt^2 Gamma_jj at t = 0 (notebook 07) = sum_{k != j} |H_kj|^2."""
    col = np.abs(H[:, j]) ** 2
    return float(col.sum() - col[j])


@dataclass
class DecayModel:
    """Level + band model with cached eigendecomposition. All transition matrices are |U|^2."""
    M: int
    delta: float
    g: float
    e0: float = 0.0
    couplings: Optional[np.ndarray] = field(default=None, repr=False)
    H: np.ndarray = field(init=False, repr=False)
    _w: np.ndarray = field(init=False, repr=False)
    _V: np.ndarray = field(init=False, repr=False)

    def __post_init__(self):
        self.H = level_band_hamiltonian(self.M, self.delta, self.g, self.e0, self.couplings)
        self._w, self._V = np.linalg.eigh(self.H)

    @property
    def rate(self) -> float:
        """Golden-rule rate 2*pi*g(e0)^2/delta, with g(e0) the coupling of the band level nearest b's energy."""
        if self.couplings is None:
            return golden_rule_rate(self.delta, self.g)
        k = np.argmin(np.abs(band_energies(self.M, self.delta) - self.e0))
        return golden_rule_rate(self.delta, float(self.couplings[k]))

    @property
    def bandwidth(self) -> float:
        return self.M * self.delta

    @property
    def recurrence_time(self) -> float:
        return 2 * np.pi / self.delta

    @property
    def nu2(self) -> float:
        return agility_squared(self.H, 0)

    def gamma(self, t: float) -> np.ndarray:
        """Full transition matrix Gamma(t <- 0), (M+1) x (M+1)."""
        U = (self._V * np.exp(-1j * self._w * t)) @ self._V.conj().T
        return np.abs(U) ** 2

    def column(self, t: float) -> np.ndarray:
        """Gamma(t <- 0) e_b: the outcome distribution for a system prepared undecayed."""
        amp = (self._V * np.exp(-1j * self._w * t)) @ self._V[0].conj()
        return np.abs(amp) ** 2

    def survival(self, t) -> np.ndarray:
        """P(t) = Gamma_bb(t <- 0), vectorised over t."""
        t = np.atleast_1d(np.asarray(t, dtype=float))
        amp = (np.abs(self._V[0]) ** 2) @ np.exp(-1j * np.outer(self._w, t))
        return np.abs(amp) ** 2


def coarse_gamma(P: float, M: int) -> np.ndarray:
    """
    2 x 2 coarse-grained Gamma on {undecayed, decayed}, from the survival P = Gamma_bb.
    The 'decayed' column starts from a uniform mixture of the M band levels (a choice: the coarse process is only
    defined once that weighting is fixed). Its entry back to b is mean_k Gamma_bk = (1 - P)/M, because the row
    b of |U|^2 also sums to 1 (U is unitary).
    """
    q = (1 - P) / M
    return np.array([[P, q], [1 - P, 1 - q]])


def negative_mass(D: np.ndarray) -> float:
    """Largest total negative weight in any column of D (0 when D is stochastic)."""
    return float(-np.clip(D, None, 0).sum(axis=0).min()) if np.any(D < 0) else 0.0


def division_defect(model: DecayModel, t1: float, s: float) -> dict:
    """
    What a single division event at t1 changes, for a system prepared in b, after a further time s.

    Without the event: Gamma(t1 + s) e_b.  With it: Gamma(s) Gamma(t1) e_b.
    Returns
      survival      Delta_bb = P(t1+s) - [Gamma(s) Gamma(t1)]_bb  (= factorization - reexcitation)
      factorization P(t1+s) - P(t1) P(s)        zero iff survival is exponential
      reexcitation  sum_k Gamma_bk(s) Gamma_kb(t1)  band levels, set loose at t1, returning to b
      band_l1       L1 change of the band populations (invisible to a decayed-or-not observer)
      total_l1      L1 change of the whole column
    """
    Gs, p1 = model.gamma(s), model.column(t1)
    with_event = Gs @ p1
    without = model.column(t1 + s)
    P1, Ps, P12 = p1[0], Gs[0, 0], without[0]
    reex = float((Gs[0, 1:] * p1[1:]).sum())
    return {
        "survival": float(P12 - with_event[0]),
        "factorization": float(P12 - P1 * Ps),
        "reexcitation": reex,
        "band_l1": float(np.abs(without[1:] - with_event[1:]).sum()),
        "total_l1": float(np.abs(without - with_event).sum()),
    }


def asymptotic_decay(model: DecayModel, t1: float, t2: float, n: int = 200):
    """
    Read the long-time decay off Gamma alone: fit ln P(t) = ln Z - kappa*t over [t1, t2].
    Returns (kappa, Z). kappa can differ from the golden-rule estimate (level shift, structured bands).
    """
    t = np.linspace(t1, t2, n)
    slope, intercept = np.polyfit(t, np.log(model.survival(t)), 1)
    return float(-slope), float(np.exp(intercept))


def survival_with_records(model: DecayModel, tau: float, eps: float, n_events: int) -> np.ndarray:
    """
    Survival after each of n_events records spaced tau apart, starting in b.

    A record of strength eps multiplies every off-diagonal element of the density matrix (configuration basis) by
    (1 - eps): phase damping, as in notebooks 06 and 08. eps = 1 is a full division event, so the result equals
    the chain Gamma(tau)^n applied to e_b (Barandes, Correspondence eq. 57); eps = 0 is no record at all.
    Returns an array of length n_events + 1 (index 0 is t = 0).
    """
    U = (model._V * np.exp(-1j * model._w * tau)) @ model._V.conj().T
    rho = np.zeros((model.M + 1, model.M + 1), dtype=complex)
    rho[0, 0] = 1.0
    out = [1.0]
    for _ in range(n_events):
        rho = U @ rho @ U.conj().T
        diag = np.diag(np.diag(rho))
        rho = (1 - eps) * rho + eps * diag
        out.append(rho[0, 0].real)
    return np.array(out)
