import numpy as np
from scipy.linalg import expm
from isp.spinor import (axis_loop, belt_family, concat, detector_probs, divisible_detector_probs, gamma,
                        interferometer_law, is_permutation, kochen_specker_up_prob, law_from_path, random_loop,
                        rotation_vector, so3, so3_of, su2)


def test_z_rotation_is_invisible_to_isolated_gamma():
    for ang in [0.3, np.pi, 2 * np.pi, 3 * np.pi, 4 * np.pi]:
        np.testing.assert_allclose(gamma(su2([0, 0, 1], ang)), np.eye(2), atol=1e-12)


def test_isolated_gamma_has_period_2pi_but_law_has_4pi():
    for axis in ([0, 1, 0], [1, 2, 3]):
        np.testing.assert_allclose(gamma(su2(axis, 2 * np.pi)), np.eye(2), atol=1e-12)
        np.testing.assert_allclose(su2(axis, 2 * np.pi), -np.eye(2), atol=1e-12)
        np.testing.assert_allclose(su2(axis, 4 * np.pi), np.eye(2), atol=1e-12)


def test_sign_is_gauge_for_isolated_spin():
    U = su2([1, -1, 2], 1.3)
    np.testing.assert_allclose(gamma(U), gamma(-U))
    np.testing.assert_allclose(so3_of(U), so3_of(-U), atol=1e-12)


def test_so3_of_matches_rodrigues():
    np.testing.assert_allclose(so3_of(su2([1, 2, 3], 0.9)), so3([1, 2, 3], 0.9), atol=1e-12)


def test_interferometer_period_4pi():
    for phi in np.linspace(0, 4 * np.pi, 9):
        p = detector_probs(su2([0, 0, 1], phi))
        assert abs(p["O"] - np.cos(phi / 4) ** 2) < 1e-12
        assert abs(p["O"] + p["H"] - 1) < 1e-12


def test_interferometer_law_unitary():
    L = interferometer_law(su2([0, 1, 0], 0.7))
    np.testing.assert_allclose(L.conj().T @ L, np.eye(4), atol=1e-12)


def test_divisible_prediction_is_flat():
    for G in (np.eye(2), gamma(su2([0, 1, 0], 1.0)), np.full((2, 2), 0.5)):
        p = divisible_detector_probs(G)
        assert abs(p["O"] - 0.5) < 1e-12


def test_law_from_path_matches_closed_form():
    np.testing.assert_allclose(law_from_path(axis_loop([0, 0, 1], 0.5)), su2([0, 0, 1], np.pi), atol=1e-10)
    np.testing.assert_allclose(law_from_path(axis_loop([0, 0, 1], 1)), -np.eye(2), atol=1e-10)


def test_belt_family_is_closed_and_detector_constant():
    for beta in np.linspace(0, 1.5, 7):
        Rs = belt_family(beta)
        np.testing.assert_allclose(Rs[0], Rs[-1], atol=1e-10)
        assert detector_probs(law_from_path(Rs))["O"] > 1 - 1e-9


def test_one_turn_class_survives_concatenation_with_belt():
    for beta in np.linspace(0, 1.5, 4):
        Rs = concat(belt_family(beta), axis_loop([0, 0, 1], 1))
        assert detector_probs(law_from_path(Rs))["H"] > 1 - 1e-9


def test_random_closed_loops_give_binary_detector():
    rng = np.random.default_rng(3)
    for _ in range(10):
        Rs = random_loop(rng)
        np.testing.assert_allclose(Rs[0], Rs[-1], atol=1e-10)
        pO = detector_probs(law_from_path(Rs))["O"]
        assert min(pO, 1 - pO) < 1e-9


def test_kochen_specker_reproduces_cos2_half_angle():
    for th in [0.4, 1.2, 2.0, 2.8]:
        assert abs(kochen_specker_up_prob(th) - np.cos(th / 2) ** 2) < 5e-3


def test_rotation_gamma_is_not_a_homogeneous_semigroup():
    G = lambda t: gamma(su2([0, 1, 0], t))
    assert not np.allclose(G(0.7) @ G(1.1), G(1.8))


def test_rotation_divisible_below_90_degrees_not_beyond():
    G = lambda t: gamma(su2([0, 1, 0], t))
    assert (G(1.4) @ np.linalg.inv(G(0.6))).min() > -1e-12          # both turns < 90 degrees: stochastic middle factor
    assert (G(2.0) @ np.linalg.inv(G(1.5))).min() < -0.1            # straddling 90 degrees: no stochastic middle factor
    for s, t in [(0.3, 1.2), (1.0, 2.0), (1.5, 2.0), (2.5, 3.0)]:     # stochastic iff |cos t| <= |cos s|
        ok = (G(t) @ np.linalg.inv(G(s))).min() > -1e-12
        assert ok == (abs(np.cos(t)) <= abs(np.cos(s)))


def test_phase_shifted_law_same_isolated_gamma_but_no_720_effect():
    for phi in np.linspace(0, 4 * np.pi, 9):
        Tp = np.exp(1j * phi / 2) * su2([0, 0, 1], phi)
        np.testing.assert_allclose(gamma(Tp), gamma(su2([0, 0, 1], phi)), atol=1e-12)
        assert abs(detector_probs(Tp)["O"] - 1) < 1e-12


def test_rotation_vector_near_pi():
    for ang in [np.pi - 1e-6, np.pi, 3.0]:
        R = so3([1, 2, -1], ang)
        w = rotation_vector(R)
        np.testing.assert_allclose(so3(w, np.linalg.norm(w)), R, atol=1e-9)


def test_random_markov_generator_not_periodic():
    rng = np.random.default_rng(1)
    A = rng.random((3, 3)); np.fill_diagonal(A, 0)
    L = A - np.diag(A.sum(0))
    for t in [0.5, 2.0, 8.0]:
        assert not is_permutation(expm(L * t))
