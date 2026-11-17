import numpy as np
from isp.wick import (euclidean_markov, hopping_hamiltonian, is_stoquastic, negative_mass, real_gamma,
                      stoquastic_gauge, two_particle_hamiltonian)


def test_euclidean_is_markov_semigroup_for_stoquastic():
    H = hopping_hamiltonian(6, potential=np.linspace(-1, 1, 6))
    Pa, psi = euclidean_markov(H, 0.4)
    Pb, _ = euclidean_markov(H, 0.7)
    Pab, _ = euclidean_markov(H, 1.1)
    assert Pa.min() >= 0 and np.all(psi > 0)
    np.testing.assert_allclose(Pa.sum(axis=0), 1, atol=1e-12)
    np.testing.assert_allclose(Pab, Pb @ Pa, atol=1e-12)
    np.testing.assert_allclose(Pa @ psi ** 2, psi ** 2, atol=1e-12)


def test_real_gamma_blind_to_gauge_and_sign_of_H():
    H = hopping_hamiltonian(5, potential=np.linspace(-1, 1, 5))
    d = np.array([1, -1, 1, 1, -1.0])
    G = real_gamma(H, 0.8)
    np.testing.assert_allclose(real_gamma(d[:, None] * H * d[None, :], 0.8), G, atol=1e-12)
    np.testing.assert_allclose(real_gamma(-H, 0.8), G, atol=1e-12)


def test_frustrated_ring_has_no_stoquastic_gauge():
    assert stoquastic_gauge(-hopping_hamiltonian(4, ring=True)) is not None     # even ring, + hopping: bipartite
    assert stoquastic_gauge(-hopping_hamiltonian(5, ring=True)) is None         # odd ring, + hopping: frustrated
    P, _ = euclidean_markov(-hopping_hamiltonian(5, ring=True), 1.0)
    assert P.min() < 0


def test_fermions_equal_bosons_on_open_chain_not_ring():
    v = np.array([0.3, -0.5, 0.8, -0.1, 0.4])
    Hb, _ = two_particle_hamiltonian(5, ring=False, fermion=False, potential=v)
    Hf, _ = two_particle_hamiltonian(5, ring=False, fermion=True, potential=v)
    np.testing.assert_allclose(Hf, Hb)
    Hb, _ = two_particle_hamiltonian(5, ring=True, fermion=False, potential=v)
    Hf, _ = two_particle_hamiltonian(5, ring=True, fermion=True, potential=v)
    assert not np.allclose(real_gamma(Hb, 0.9), real_gamma(Hf, 0.9))
    assert is_stoquastic(Hb) and stoquastic_gauge(Hf) is None


def test_negative_mass():
    assert negative_mass(np.eye(3)) == 0.0
    assert abs(negative_mass(np.array([[1.3, 0.0], [-0.3, 1.0]])) - 0.3) < 1e-12
