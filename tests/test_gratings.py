import numpy as np
from scipy.special import jv
from isp.divisibility import _intermediate_lp
from isp.gratings import (KAPPA_WALL, TALBOT, char_fn, divisor_kernel, far_weights, flight, gamma, grating, grid,
                          negative_mass, record, two_gratings)


def test_bessel_kernel_and_amplitude_composition():
    M = 48
    _, p, _ = grid(M)
    np.testing.assert_allclose(gamma(grating(1.5, M))[:, 0], jv(p, 1.5) ** 2, atol=1e-12)
    np.testing.assert_allclose(grating(0.4, M) @ grating(0.9, M), grating(1.3, M), atol=1e-12)
    assert np.abs(gamma(grating(1.3, M)) - gamma(grating(0.4, M)) @ gamma(grating(0.9, M))).max() > 0.05
    theta = np.linspace(0, 2 * np.pi, 7)
    direct = [np.sum(jv(np.arange(-40, 41), 1.5) ** 2 * np.exp(1j * np.arange(-40, 41) * th)).real for th in theta]
    np.testing.assert_allclose(direct, char_fn(1.5, theta), atol=1e-12)


def test_divisibility_wall_and_small_kappa_threshold():
    assert abs(jv(0, 2 * KAPPA_WALL)) < 1e-12
    assert negative_mass(1.21, 0.1) > 10 * negative_mass(1.1, 0.1)
    assert divisor_kernel(0.1, 0.1)[2] > 0 > divisor_kernel(0.1, 0.05)[2]       # threshold k2 = (sqrt3 - 1) k1
    assert negative_mass(0.1, 0.3) < 1e-12
    M = 48
    lp = lambda k1, k2: _intermediate_lp(gamma(grating(k1 + k2, M)), gamma(grating(k1, M)), True)[1]
    assert lp(0.1, 0.3) < 1e-6 and lp(1.5, 1.5) > 1


def test_far_weights_alternate_so_never_exactly_divisible():
    # the contour-shifted weights agree with the direct FFT where the latter is above round-off
    q = divisor_kernel(0.3, 1.0, 2048)
    np.testing.assert_allclose(far_weights(0.3, 1.0, [1, 2, 3]), q[[1, 2, 3]], rtol=1e-6)
    # far weights alternate in sign: negative mass exists even where double precision reports ~0
    w = far_weights(0.3, 1.0, range(10, 20))
    assert np.all(np.sign(w[:-1]) != np.sign(w[1:])) and (w < 0).any()
    # above the q_2 sign change, q_4 is still negative at a size double precision resolves
    assert divisor_kernel(0.5, 0.5)[2] > 0 and divisor_kernel(0.5, 0.5)[4] < -1e-7


def test_talbot_flight_does_nothing_yet_everything():
    M, k = 64, 1.5
    np.testing.assert_allclose(gamma(flight(1.234, M)), np.eye(M), atol=1e-15)
    markov = (gamma(grating(k, M)) @ gamma(grating(k, M)))[0, 0]
    assert abs(markov - np.sum(jv(np.arange(-30, 31), k) ** 4)) < 1e-12
    assert abs(two_gratings(k, k, TALBOT / 2)[0] - 1) < 1e-12
    assert abs(two_gratings(k, k, TALBOT)[0] - jv(0, 2 * k) ** 2) < 1e-12


def test_records():
    k = 1.5
    markov = (gamma(grating(k, 64)) @ gamma(grating(k, 64)))[0, 0]
    assert abs(two_gratings(k, k, TALBOT / 2, eps=1)[0] - markov) < 1e-12
    assert abs(two_gratings(k, k, TALBOT / 2, eps=0.5)[0] - (0.5 + 0.5 * markov)) < 1e-12
    coarse = two_gratings(k, k, TALBOT / 2, eps=1, basis="position", ell=10.0)[0]
    fine = two_gratings(k, k, TALBOT / 2, eps=1, basis="position", ell=0.3)[0]
    assert coarse > 0.95 and fine < markov
    rho = np.zeros((64, 64), dtype=complex); rho[0, 0] = 1
    U = flight(TALBOT / 4, 64) @ grating(k, 64)
    for ell in (1.0, 3.0, 10.0):                                   # the record is a valid channel: rho stays positive
        assert np.linalg.eigvalsh(record(U @ rho @ U.conj().T, 1.0, "position", ell)).min() > -1e-12
