import numpy as np
from scipy.linalg import expm
from scipy.stats import unitary_group
from isp.identical import chain, classical_generator, configurations, embed, gamma, stationary


def test_column_stochastic_and_two_particle_average():
    U = unitary_group.rvs(4, random_state=3)
    GB, CB = gamma(U, 2, "boson")
    GF, CF = gamma(U, 2, "fermion")
    GD, _ = gamma(U, 2, "distinguishable")
    for G in (GB, GF, GD):
        np.testing.assert_allclose(G.sum(axis=0), 1, atol=1e-12)
    distinct = [b for b, c in enumerate(CB) if max(c) == 1]
    avg = (GB + embed(GF, CF, CB)) / 2
    np.testing.assert_allclose(GD[:, distinct], avg[:, distinct], atol=1e-12)


def test_hong_ou_mandel():
    BS = np.array([[1, 1j], [1j, 1]]) / np.sqrt(2)
    expected = {"boson": 0.0, "distinguishable": 0.5, "fermion": 1.0}
    for kind, coincidence in expected.items():
        G, C = gamma(BS, 2, kind)
        assert abs(G[C.index((1, 1)), C.index((1, 1))] - coincidence) < 1e-12


def test_dense_records_converge_to_classical_process():
    h, s = chain(4), 0.6
    for kind in ("boson", "fermion", "distinguishable"):
        L, _ = classical_generator(h, 2, kind)
        errs = []
        for tau in (0.1, 0.05):
            G, _ = gamma(expm(-1j * h * tau), 2, kind)
            errs.append(np.abs(np.linalg.matrix_power(G, int(round(s / tau ** 2))) - expm(s * L)).max())
        assert errs[1] < errs[0] / 3 and errs[1] < 1e-3


def test_stationary_counting():
    h = chain(3)
    pB = stationary(classical_generator(h, 2, "boson")[0])
    pF = stationary(classical_generator(h, 2, "fermion")[0])
    pD, C = stationary(classical_generator(h, 2, "distinguishable")[0]), configurations(3, 2, "distinguishable")
    np.testing.assert_allclose(pB, 1 / 6, atol=1e-10)                 # Bose-Einstein: every occupation equally likely
    np.testing.assert_allclose(pF, 1 / 3, atol=1e-10)                 # Fermi-Dirac
    np.testing.assert_allclose(pD, [1 / 9 if max(c) == 2 else 2 / 9 for c in C], atol=1e-10)   # Maxwell-Boltzmann
