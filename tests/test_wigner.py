import numpy as np
from scipy.linalg import expm
from isp.wigner import DiscretePhaseSpace, indivisibility_defect, is_permutation, negative_mass


def random_unitary(d, seed, t=0.5):
    rng = np.random.default_rng(seed)
    H = rng.normal(size=(d, d)) + 1j * rng.normal(size=(d, d))
    return expm(-1j * (H + H.conj().T) * t)


def test_marginals_and_configuration_states():
    ps = DiscretePhaseSpace(5)
    rho = np.zeros((5, 5)); rho[2, 2] = 1
    W = ps.wigner(rho)
    np.testing.assert_allclose(W[2], 0.2)
    np.testing.assert_allclose(np.delete(W, 2, axis=0), 0, atol=1e-12)
    psi = np.ones(5, dtype=complex) / np.sqrt(5); psi[1] *= 1j
    rho = np.outer(psi, psi.conj())
    np.testing.assert_allclose(ps.wigner(rho).sum(axis=1), np.diag(rho).real, atol=1e-12)


def test_wigner_map_composes_and_marginal_is_gamma():
    ps = DiscretePhaseSpace(5)
    U1, U2 = random_unitary(5, 1), random_unitary(5, 2)
    M1, M2, M12 = ps.wigner_map(U1), ps.wigner_map(U2), ps.wigner_map(U2 @ U1)
    np.testing.assert_allclose(M1.sum(axis=0), 1, atol=1e-12)
    np.testing.assert_allclose(M12, M2 @ M1, atol=1e-12)
    np.testing.assert_allclose(ps.marginal @ M1 @ ps.lift, np.abs(U1) ** 2, atol=1e-12)


def test_clifford_is_permutation_cubic_is_negative():
    ps = DiscretePhaseSpace(5)
    for U in (ps.fourier(), ps.shear(), ps.X, ps.fourier() @ ps.shear()):
        assert is_permutation(ps.wigner_map(U))
    assert negative_mass(ps.wigner_map(ps.cubic())) > 0.1


def test_independence_both_directions():
    ps = DiscretePhaseSpace(5)
    F, C = ps.fourier(), ps.cubic()
    assert indivisibility_defect(np.abs(F) ** 2, np.abs(F @ F) ** 2) > 0.5      # Clifford, yet indivisible
    assert indivisibility_defect(np.abs(C) ** 2, np.abs(C @ C) ** 2) == 0.0     # Wigner-negative, yet divisible
