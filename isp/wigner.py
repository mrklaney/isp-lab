# wigner.py
"""
Discrete Wigner function on a d x d phase space, d odd (notebook 13).

Configurations are q = 0..d-1 (the computational basis); the extra phase-space coordinate is a "momentum" p = 0..d-1.
Phase-point operators A(q, p) = D(q, p) A0 D(q, p)^dagger, with A0|x> = |-x> (parity) and D the displacement
operators, give W(q, p) = Tr(rho A(q, p)) / d (Wootters 1987; Gross 2006). Properties used:
- summing W over p gives the configuration probabilities <q|rho|q>;
- a configuration |q0><q0| has W = 1/d on the line q = q0 and 0 elsewhere (non-negative);
- a unitary U acts on W as the d^2 x d^2 matrix M(U)_{ab} = Tr(A_a U A_b U^dagger) / d, whose columns sum to 1 and
  which composes exactly, M(U2 U1) = M(U2) M(U1), but which can have negative entries;
- Clifford unitaries (Fourier, shear, shifts) give permutation matrices M.
"""

from typing import List, Tuple
import numpy as np

from .divisibility import _intermediate_lp


class DiscretePhaseSpace:
    """Phase space Z_d x Z_d for odd d, with points ordered (q, p) -> d*q + p."""

    def __init__(self, d: int):
        if d % 2 == 0:
            raise ValueError("d must be odd")
        self.d = d
        self.omega = np.exp(2j * np.pi / d)
        self.half = pow(2, -1, d)          # the inverse of 2 modulo d
        self.X = np.roll(np.eye(d), 1, axis=0)                 # X|x> = |x+1>
        self.Z = np.diag(self.omega ** np.arange(d))           # Z|x> = w^x |x>
        A0 = np.zeros((d, d))
        for x in range(d):
            A0[(-x) % d, x] = 1
        self.points: List[Tuple[int, int]] = [(q, p) for q in range(d) for p in range(d)]
        self.A = []
        for q, p in self.points:
            D = self.displacement(q, p)
            self.A.append(D @ A0 @ D.conj().T)
        # marginal over p (phase space -> configurations) and uniform lift (configurations -> phase space)
        self.marginal = np.zeros((d, d * d))
        self.lift = np.zeros((d * d, d))
        for k, (q, p) in enumerate(self.points):
            self.marginal[q, k] = 1.0
            self.lift[k, q] = 1.0 / d

    def displacement(self, q: int, p: int) -> np.ndarray:
        d = self.d
        return (self.omega ** (-self.half * q * p) * np.linalg.matrix_power(self.Z, p)
                @ np.linalg.matrix_power(self.X, q))

    def wigner(self, rho: np.ndarray) -> np.ndarray:
        """W as a d x d array indexed [q, p]."""
        return np.array([np.trace(rho @ a).real / self.d for a in self.A]).reshape(self.d, self.d)

    def wigner_map(self, U: np.ndarray) -> np.ndarray:
        """M(U): how U moves the Wigner function, as a d^2 x d^2 matrix (columns sum to 1)."""
        Ud = U.conj().T
        return np.array([[np.trace(a @ U @ b @ Ud).real / self.d for b in self.A] for a in self.A])

    # ---- standard gates
    def fourier(self) -> np.ndarray:
        d = self.d
        return np.array([[self.omega ** (j * k) for k in range(d)] for j in range(d)]) / np.sqrt(d)

    def shear(self) -> np.ndarray:
        """Quadratic phase: a Clifford gate (the discrete analogue of a quadratic potential)."""
        return np.diag(self.omega ** (self.half * np.arange(self.d) ** 2))

    def cubic(self) -> np.ndarray:
        """Cubic phase: not Clifford for d >= 5 (for d = 3, x^3 = x mod 3 makes it a Clifford shift)."""
        return np.diag(self.omega ** (np.arange(self.d) ** 3))


def negative_mass(M: np.ndarray, tol: float = 1e-10) -> float:
    """Largest total negative weight in any column (0 for a matrix with no negative entries)."""
    return float(-np.clip(M, None, 0).sum(axis=0).min()) if np.any(M < -tol) else 0.0


def is_permutation(M: np.ndarray, tol: float = 1e-9) -> bool:
    return bool(np.all((np.abs(M) < tol) | (np.abs(M - 1) < tol)) and np.allclose(M.sum(axis=0), 1)
                and np.allclose(M.sum(axis=1), 1))


def indivisibility_defect(G_first: np.ndarray, G_both: np.ndarray) -> float:
    """
    Smallest L1 residual || D G_first - G_both ||_1 over stochastic D (a linear program; no inverse needed).
    0 exactly when a stochastic intermediate exists.
    """
    _, residual, _ = _intermediate_lp(G_both, G_first, minimize_residual=True)
    return 0.0 if residual < 1e-8 else residual
