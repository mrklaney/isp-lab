import numpy as np
from scipy.linalg import expm
from isp.loops import (energy_basis, field_hamiltonian, fringe_phase, gamma, loop_unitary, recorded, ring_hamiltonian,
                       solid_angle)


def test_gamma_depends_only_on_flux():
    H1, H2 = ring_hamiltonian(6, 0.9, gauge="uniform"), ring_hamiltonian(6, 0.9)
    D = np.diag(np.exp(1j * np.random.default_rng(0).uniform(0, 2 * np.pi, 6)))
    for H in (H2, D @ H1 @ D.conj().T):
        np.testing.assert_allclose(gamma(H, 1.3), gamma(H1, 1.3), atol=1e-12)
    np.testing.assert_allclose(gamma(ring_hamiltonian(6, 0.9 + 2 * np.pi), 1.3), gamma(H1, 1.3), atol=1e-12)
    assert np.abs(gamma(ring_hamiltonian(6, 0.0), 1.3) - gamma(H1, 1.3)).max() > 0.01


def test_flux_sign_and_bipartite_blindness():
    for N in (5, 6):
        G, Gm = gamma(ring_hamiltonian(N, 0.7), 1.0), gamma(ring_hamiltonian(N, -0.7), 1.0)
        np.testing.assert_allclose(Gm, G.T, atol=1e-12)
    G6 = gamma(ring_hamiltonian(6, 0.7), 1.0)
    np.testing.assert_allclose(G6, G6.T, atol=1e-12)                       # even ring: cannot see the sign
    G5 = gamma(ring_hamiltonian(5, 0.7), 1.0)
    assert np.abs(G5 - G5.T).max() > 0.05                                  # odd ring: can


def test_opposite_site_interference_and_records():
    tau = 0.05
    base = gamma(ring_hamiltonian(6, 0.0), tau)[3, 0]
    for f in (np.pi / 3, np.pi / 2, np.pi):
        assert abs(gamma(ring_hamiltonian(6, f), tau)[3, 0] / base - np.cos(f / 2) ** 2) < 1e-3
    d = [np.abs(recorded(ring_hamiltonian(6, 0.0), t, 1.0) - recorded(ring_hamiltonian(6, np.pi), t, 1.0)).max()
         for t in (0.1, 0.05)]
    assert d[1] < d[0] / 8


def test_berry_fringe_shift_and_adiabatic_identity():
    T, th = 2000.0, np.pi / 6
    x = np.linspace(400, 404, 61)
    Pl = [abs(loop_unitary(v / T, th, T)[1, 0]) ** 2 for v in x]
    Ps = [abs(expm(-1j * field_hamiltonian(v / T, th) * T)[1, 0]) ** 2 for v in x]
    shift = np.mod(fringe_phase(x, np.array(Pl))[0] - fringe_phase(x, np.array(Ps))[0], 2 * np.pi)
    assert abs(shift - solid_angle(th)) < 0.02
    V = energy_basis(1.0, th)
    Gm = np.abs(V.conj().T @ loop_unitary(1.0, th, T) @ V) ** 2
    assert Gm[1, 0] < 1e-5
