import numpy as np
from isp.spectrum import (SpectralModel, distinguishability, is_permutation, radial_hydrogen_hamiltonian,
                          record_chain, revival, ring_hamiltonian)


def hydrogen(R=40.0, h=0.1, Z=1.0):
    H, r = radial_hydrogen_hamiltonian(h, R, Z)
    return SpectralModel(H), r


def test_hydrogen_levels_approach_rydberg():
    m, _ = hydrogen()
    np.testing.assert_allclose(m.E[:3], [-0.5, -0.125, -1 / 18], rtol=3e-3)


def test_gamma_doubly_stochastic_and_symmetric_for_real_H():
    m, _ = hydrogen()
    G = m.gamma(7.3)
    np.testing.assert_allclose(G.sum(0), 1, atol=1e-10)
    np.testing.assert_allclose(G.sum(1), 1, atol=1e-10)
    np.testing.assert_allclose(G, G.T, atol=1e-12)


def test_columns_and_entry_match_gamma():
    m, _ = hydrogen()
    ts = [0.0, 2.5, 11.0]
    C = m.columns(9, ts)
    for k, t in enumerate(ts):
        np.testing.assert_allclose(C[:, k], m.gamma(t)[:, 9], atol=1e-12)
    np.testing.assert_allclose(m.entry(4, 9, ts), C[4], atol=1e-12)


def test_lines_reconstruct_gamma_entry():
    rng = np.random.default_rng(0)
    A = rng.normal(size=(6, 6)); m = SpectralModel(A + A.T)
    a = m.weights(1, 3)
    for t in [0.4, 3.1, 17.0]:
        nn, mm = np.triu_indices(6, 1)
        val = np.sum(a ** 2) + np.sum(2 * a[nn] * a[mm] * np.cos((m.E[nn] - m.E[mm]) * t))
        assert abs(val - m.entry(1, 3, [t])[0]) < 1e-12
    freq, w, c0 = m.lines(1, 3)
    assert abs(c0 - np.sum(a ** 2)) < 1e-14 and len(freq) == 15


def test_time_average_and_variance_formulas():
    rng = np.random.default_rng(1)
    A = rng.normal(size=(5, 5)); m = SpectralModel(A + A.T)
    ts = np.linspace(0, 40000, 400001)
    g = m.entry(2, 2, ts)
    assert abs(g.mean() - m.time_average(2, 2)) < 2e-3
    assert abs(g.var() - m.time_variance(2, 2)) < 2e-3


def test_bound_memory_independent_of_box_continuum_falls_as_one_over_R():
    j = 9  # r = 1 bohr
    out = {}
    for R in (40.0, 160.0):
        m, _ = hydrogen(R=R)
        b = m.E < 0
        out[R] = (m.time_average(j, j, b), m.time_average(j, j, ~b))
    assert abs(out[40.0][0] - out[160.0][0]) < 1e-4 * 30
    np.testing.assert_allclose(out[40.0][1] / out[160.0][1], 4.0, rtol=0.05)


def test_divisible_chain_never_revives_and_unitary_one_does():
    m, _ = hydrogen()
    ts = np.linspace(0, 200, 2001)
    D = distinguishability(m.columns(9, ts), m.columns(29, ts))
    assert revival(D) > 0.05
    G = m.gamma(0.5)
    Dc = [distinguishability(record_chain(G, n)[:, 9], record_chain(G, n)[:, 29]) for n in range(0, 60)]
    assert revival(np.array(Dc)) < 1e-12


def test_ring_twist_changes_gamma_and_is_periodic():
    m0, ma, ma1 = (SpectralModel(ring_hamiltonian(7, a)) for a in (0.0, 0.3, 1.3))
    diff = max(np.abs(m0.gamma(t) - ma.gamma(t)).max() for t in np.linspace(0.1, 5, 50))
    assert diff > 0.05
    np.testing.assert_allclose(ma.gamma(2.2), ma1.gamma(2.2), atol=1e-12)
    np.testing.assert_allclose(np.sort(ma.E), np.sort(-2 * np.cos(2 * np.pi * (np.arange(7) + 0.3) / 7)), atol=1e-12)


def test_is_permutation():
    assert is_permutation(np.eye(3)[[1, 2, 0]])
    assert not is_permutation(np.full((2, 2), 0.5))


def test_time_variance_groups_degenerate_gaps():
    m, _ = hydrogen(R=4.0, Z=0.0)                     # symmetric box spectrum: many coinciding gaps
    ts = np.random.default_rng(0).uniform(0, 1e6, 20000)
    np.testing.assert_allclose(m.time_variance(9, 9), m.entry(9, 9, ts).var(), rtol=0.05)


def test_time_variance_distinct_gaps_formula():
    rng = np.random.default_rng(2)
    A = rng.normal(size=(6, 6)); m = SpectralModel(A + A.T)
    a2 = np.abs(m.weights(1, 1)) ** 2
    np.testing.assert_allclose(m.time_variance(1, 1), a2.sum() ** 2 - (a2 ** 2).sum(), rtol=1e-10)


def test_ring_gamma_symmetric_under_alpha_to_half_n_minus_alpha():
    for N, a in [(7, 0.1), (8, 0.2), (5, 0.37)]:
        A, B = SpectralModel(ring_hamiltonian(N, a)), SpectralModel(ring_hamiltonian(N, N / 2 - a))
        for t in (0.4, 1.7, 5.0):
            np.testing.assert_allclose(A.gamma(t), B.gamma(t), atol=1e-12)


def test_unistochastic_returning_to_permutation_is_divisible_there():
    m = SpectralModel(np.array([[0.0, 1.0], [1.0, 0.0]]))   # sigma_x: Gamma(pi) = I
    assert is_permutation(m.gamma(np.pi)) and not is_permutation(m.gamma(0.3))
