import numpy as np
from isp.decay import (DecayModel, agility_squared, coarse_gamma, division_defect,
                       golden_rule_rate, level_band_hamiltonian, negative_mass)


def small():
    return DecayModel(M=200, delta=0.05, g=0.02)


def test_hamiltonian_shape_and_coupling():
    H = level_band_hamiltonian(4, 1.0, 0.3)
    assert H.shape == (5, 5)
    np.testing.assert_allclose(H[0, 1:], 0.3)
    np.testing.assert_allclose(np.diag(H)[1:], [-1.5, -0.5, 0.5, 1.5])


def test_gamma_is_stochastic_and_column_matches():
    m = small()
    G = m.gamma(3.0)
    np.testing.assert_allclose(G.sum(axis=0), 1, atol=1e-12)
    np.testing.assert_allclose(m.column(3.0), G[:, 0], atol=1e-12)
    np.testing.assert_allclose(m.survival([3.0])[0], G[0, 0], atol=1e-12)


def test_agility_matches_curvature():
    m = small()
    h = 1e-3
    P = m.survival([-h, 0, h])
    nu2_num = -0.5 * (P[0] - 2 * P[1] + P[2]) / h ** 2
    assert abs(nu2_num - m.nu2) < 1e-6
    assert abs(agility_squared(m.H) - m.M * m.g ** 2) < 1e-12


def test_golden_rule_rate_in_window():
    m = small()
    t = np.array([10.0, 10.01])
    P = m.survival(t)
    r = -np.diff(np.log(P))[0] / 0.01
    assert abs(r / golden_rule_rate(m.delta, m.g) - 1) < 0.05


def test_defect_identity_and_zeno_slope():
    m = small()
    d = division_defect(m, 0.02, 0.02)
    assert abs(d["survival"] - (d["factorization"] - d["reexcitation"])) < 1e-12
    assert abs(d["survival"] / (-2 * m.nu2 * 0.02 * 0.02) - 1) < 0.01


def test_coarse_gamma_stochastic_and_negative_mass():
    m = small()
    G = m.gamma(5.0)
    C = coarse_gamma(G[0, 0], m.M)
    np.testing.assert_allclose(C.sum(axis=0), 1, atol=1e-12)
    assert abs(C[0, 1] - G[0, 1:].mean()) < 1e-14
    assert negative_mass(np.eye(2)) == 0.0
    assert negative_mass(np.array([[1.2, 0], [-0.2, 1]])) > 0.19


def test_structured_band_rate_and_flat_default():
    from isp.decay import lorentzian_couplings
    gk = lorentzian_couplings(400, 0.05, 0.03, 2.0, 0.5)
    m = DecayModel(M=400, delta=0.05, g=0.03, couplings=gk)
    k = np.argmin(np.abs((np.arange(400) - 199.5) * 0.05))
    assert abs(m.rate - golden_rule_rate(0.05, gk[k])) < 1e-15
    np.testing.assert_allclose(m.H[0, 1:], gk)


def test_asymptotic_decay_flat():
    from isp.decay import asymptotic_decay
    m = DecayModel(M=1000, delta=0.01, g=np.sqrt(0.1 * 0.01 / (2 * np.pi)))
    kappa, Z = asymptotic_decay(m, 20, 50)
    assert abs(kappa / 0.1 - 1) < 0.01
    assert abs(Z - (1 + 4 / np.pi * 0.01)) < 0.002


def test_records_full_strength_is_gamma_chain_and_zero_is_free():
    from isp.decay import survival_with_records
    m = small()
    s = survival_with_records(m, 0.5, 1.0, 6)
    p = np.zeros(m.M + 1); p[0] = 1
    G = m.gamma(0.5)
    for _ in range(6):
        p = G @ p
    assert abs(s[-1] - p[0]) < 1e-12
    s0 = survival_with_records(m, 0.5, 0.0, 6)
    assert abs(s0[-1] - m.survival([3.0])[0]) < 1e-10
