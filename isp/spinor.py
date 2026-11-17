# spinor.py
"""
Spin-1/2 rotations and the 4*pi (720 degree) periodicity read in transition matrices. Used by notebook 19.

Configurations of the spin are {up_z, down_z} (index 0, 1). The rotation the field applies to the spin (the accumulated
precession) is a path R(s) in SO(3), s in [0, 1]. It is not the direction the field points: a closed loop of field
directions gives a Berry phase instead. The law is driven by R(s): on a short step the field rotates the spin by the rotation vector
w_k = log(R_{k+1} R_k^T), so Theta_{k+1} = exp(-i w_k . sigma / 2) Theta_k (a spin precessing in a field, omega = gamma B).
Gamma = |Theta|^2 entrywise.

The two-path interferometer has configurations (arm, spin) with arm in {A, B}: index 2*arm + spin. A balanced beam splitter
sends the particle into both arms, arm A carries the rotation, arm B does not, and a second beam splitter recombines them to
detectors O (arm index 0) and H (arm index 1).
"""

import numpy as np
from scipy.spatial.transform import Rotation

SX = np.array([[0, 1], [1, 0]], dtype=complex)
SY = np.array([[0, -1j], [1j, 0]], dtype=complex)
SZ = np.array([[1, 0], [0, -1]], dtype=complex)
PAULI = (SX, SY, SZ)
I2 = np.eye(2, dtype=complex)


# ---------------------------------------------------------------- rotations

def _unit(axis):
    a = np.asarray(axis, dtype=float)
    return a / np.linalg.norm(a)


def su2(axis, angle: float) -> np.ndarray:
    """exp(-i angle n.sigma / 2): the spin law for a rotation by `angle` about `axis` (period 4*pi)."""
    n = _unit(axis)
    ns = n[0] * SX + n[1] * SY + n[2] * SZ
    return np.cos(angle / 2) * I2 - 1j * np.sin(angle / 2) * ns


def so3(axis, angle: float) -> np.ndarray:
    """Rodrigues rotation matrix (period 2*pi): the physical rotation of the apparatus."""
    n = _unit(axis)
    K = np.array([[0, -n[2], n[1]], [n[2], 0, -n[0]], [-n[1], n[0], 0]])
    return np.eye(3) + np.sin(angle) * K + (1 - np.cos(angle)) * K @ K


def so3_of(U: np.ndarray) -> np.ndarray:
    """The SO(3) rotation that U in SU(2) induces: R_ab = tr(sigma_a U sigma_b U^dagger)/2. U and -U give the same R."""
    return np.array([[0.5 * np.trace(PAULI[a] @ U @ PAULI[b] @ U.conj().T).real for b in range(3)] for a in range(3)])


def rotation_vector(R: np.ndarray) -> np.ndarray:
    """log of a rotation matrix as a rotation vector, angle in [0, pi]; well conditioned near pi (scipy)."""
    return Rotation.from_matrix(R).as_rotvec()


def law_from_path(Rs) -> np.ndarray:
    """Integrate the spin law along a field history given as a sequence of SO(3) matrices (fine steps).

    Only the physical rotations enter; the sign of the result is decided by the history, not by the endpoint."""
    Th = I2.copy()
    for R0, R1 in zip(Rs[:-1], Rs[1:]):
        w = rotation_vector(R1 @ R0.T)
        ang = np.linalg.norm(w)
        if ang > 0:
            Th = su2(w, ang) @ Th
    return Th


def gamma(Theta: np.ndarray) -> np.ndarray:
    """Gamma = |Theta|^2 entrywise; columns are starting configurations."""
    return np.abs(Theta) ** 2


# ---------------------------------------------------------------- loops of rotations

def axis_loop(axis, turns: float, n: int = 400):
    """Rotation by 2*pi*turns about a fixed axis, sampled at n+1 points."""
    return [so3(axis, 2 * np.pi * turns * s) for s in np.linspace(0, 1, n + 1)]


def belt_family(beta: float, n: int = 800):
    """A loop in SO(3) for each beta in [0, pi/2]: beta = 0 is the 720 degree turn about z, beta -> pi/2 shrinks it to a
    point (Dirac's belt trick). Built from small circles through the identity on the unit-quaternion sphere, then projected
    to SO(3); every member is a closed loop of physical rotations."""
    d = np.sin(beta)
    c = np.array([np.sin(beta), np.cos(beta), 0.0]) * d          # circle centre in (w, x, z)
    u1 = np.array([np.cos(beta), -np.sin(beta), 0.0])
    u2 = np.array([0.0, 0.0, 1.0])
    rho = np.cos(beta)
    Rs = []
    for s in np.linspace(0, 1, n + 1):
        w, x, z = c + rho * (np.cos(2 * np.pi * s) * u1 + np.sin(2 * np.pi * s) * u2)
        q = np.array([w, x, z]) / np.linalg.norm([w, x, z])
        U = q[0] * I2 - 1j * (q[1] * SX + q[2] * SZ)
        Rs.append(so3_of(U))
    return Rs


def concat(*paths):
    """Concatenate paths that start at the identity: each later path is applied after the earlier ones."""
    out = list(paths[0])
    for p in paths[1:]:
        base = out[-1]
        out += [R @ base for R in p[1:]]
    return out


def random_loop(rng, corners: int = 4, steps: int = 120):
    """A random closed loop of rotations: geodesic legs I -> R_1 -> ... -> R_m -> I through random rotations."""
    pts = [np.eye(3)] + [so3(rng.normal(size=3), rng.uniform(0, np.pi)) for _ in range(corners)] + [np.eye(3)]
    Rs = [np.eye(3)]
    for R0, R1 in zip(pts[:-1], pts[1:]):
        w = rotation_vector(R1 @ R0.T)
        ang = np.linalg.norm(w)
        for t in np.linspace(0, 1, steps + 1)[1:]:
            Rs.append((so3(w, ang * t) if ang > 0 else np.eye(3)) @ R0)
    return Rs


def total_turning(Rs) -> float:
    """Total rotation angle accumulated along a path (sum of step angles), in radians."""
    return float(sum(np.linalg.norm(rotation_vector(R1 @ R0.T)) for R0, R1 in zip(Rs[:-1], Rs[1:])))


# ---------------------------------------------------------------- interferometer

BS = np.array([[1, 1], [1, -1]], dtype=complex) / np.sqrt(2)     # balanced beam splitter on the arm index


def interferometer_law(Theta_A: np.ndarray) -> np.ndarray:
    """4x4 law on (arm, spin): split, rotate spin in arm A only, recombine."""
    P_A = np.diag([1, 0]).astype(complex)
    P_B = np.diag([0, 1]).astype(complex)
    middle = np.kron(P_A, Theta_A) + np.kron(P_B, I2)
    S = np.kron(BS, I2)
    return S @ middle @ S


def detector_probs(Theta_A: np.ndarray, spin_in=(1.0, 0.0)) -> dict:
    """Probability of detector O and H for a particle entering arm A with spin distribution spin_in (over up, down).

    Uses only Gamma of the whole process: P = Gamma_total @ p_in, marginalised over spin."""
    G = gamma(interferometer_law(Theta_A))
    p_in = np.zeros(4)
    p_in[0:2] = spin_in
    p = G @ p_in
    return {"O": p[0] + p[1], "H": p[2] + p[3]}


def divisible_detector_probs(Gamma_A: np.ndarray, spin_in=(1.0, 0.0)) -> dict:
    """The same experiment if the process were divisible at the beam splitters: each stage replaced by its own Gamma."""
    P_A = np.diag([1.0, 0.0])
    P_B = np.diag([0.0, 1.0])
    M = np.kron(P_A, Gamma_A) + np.kron(P_B, np.eye(2))
    S = np.kron(gamma(BS), np.eye(2))
    p_in = np.zeros(4)
    p_in[0:2] = spin_in
    p = S @ M @ S @ p_in
    return {"O": p[0] + p[1], "H": p[2] + p[3]}


# ---------------------------------------------------------------- a classical model of Stern-Gerlach

def kochen_specker_up_prob(theta: float, samples: int = 200_000, rng=None) -> float:
    """Kochen-Specker (1967) classical model of one spin-1/2: the hidden configuration is a unit vector lam drawn on the
    hemisphere around the state direction p with density proportional to lam.p; the outcome along a is 'up' iff lam.a > 0.
    Everything is an SO(3) action on a classical vector, so a 360 degree turn restores it exactly. Returns P(up) for a at
    angle theta from p (quantum value cos^2(theta/2))."""
    rng = np.random.default_rng(0) if rng is None else rng
    u = rng.random(samples)
    ph = 2 * np.pi * rng.random(samples)
    r = np.sqrt(u)
    lam = np.stack([r * np.cos(ph), r * np.sin(ph), np.sqrt(1 - u)], axis=1)   # cosine-weighted around p = z
    a = np.array([np.sin(theta), 0.0, np.cos(theta)])
    return float(np.mean(lam @ a > 0))


# ---------------------------------------------------------------- divisible representations

def is_permutation(M: np.ndarray, tol: float = 1e-9) -> bool:
    return bool(np.all((np.abs(M) < tol) | (np.abs(M - 1) < tol)) and np.allclose(M.sum(0), 1) and np.allclose(M.sum(1), 1))
