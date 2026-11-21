import numpy as np
import pytest

from isp.eraser import (
    conditional_defect,
    idler_isometry,
    kim_model,
    path_predictability,
    sorted_visibility,
)

N = 24


@pytest.mark.parametrize("r,theta", [(0.5, np.pi / 4), (0.3, 0.2), (1.0, np.pi / 4), (0.0, 0.0)])
def test_idler_isometry_has_orthonormal_columns(r, theta):
    V = idler_isometry(r, theta)
    np.testing.assert_allclose(V.conj().T @ V, np.eye(2), atol=1e-12)


def test_joint_distribution_normalises():
    m = kim_model(N)
    assert abs(m["P_joint"].sum() - 1) < 1e-12
    np.testing.assert_allclose(m["P_x_given_d"].sum(axis=0), 1, atol=1e-12)


def test_kim_detector_rates():
    """50/50 at BS_A/BS_B and at BS: each detector fires a quarter of the time."""
    m = kim_model(N)
    np.testing.assert_allclose(m["P_detector"], 0.25, atol=1e-12)


def test_d0_singles_show_no_fringes():
    m = kim_model(N)
    np.testing.assert_allclose(m["P_screen"], 1 / N, atol=1e-12)


def test_d1_d2_fringes_are_complementary_and_d3_d4_flat():
    m = kim_model(N, slit_a=10, slit_b=13)
    k = np.arange(N)
    fringe = (1 + np.cos(2 * np.pi * k * 3 / N)) / N
    anti = (1 - np.cos(2 * np.pi * k * 3 / N)) / N
    Pxd = m["P_x_given_d"]
    np.testing.assert_allclose(Pxd[:, 0], fringe, atol=1e-12)   # R01
    np.testing.assert_allclose(Pxd[:, 1], anti, atol=1e-12)     # R02: pi shift
    np.testing.assert_allclose(Pxd[:, 2], 1 / N, atol=1e-12)    # R03: which-path
    np.testing.assert_allclose(Pxd[:, 3], 1 / N, atol=1e-12)    # R04


def test_which_path_subsets_compose_eraser_subsets_do_not():
    m = kim_model(N)
    D = conditional_defect(m)
    assert np.abs(D[:, 2:]).max() < 1e-12
    assert np.abs(D[:, :2]).max() > 1e-3


def test_defect_averages_to_zero_over_detectors():
    """Unsorted, the screen composes through the path; only sorted subsets do not."""
    m = kim_model(N, r=0.37, theta=0.6)
    D = conditional_defect(m)
    np.testing.assert_allclose(D @ m["P_detector"], 0, atol=1e-12)


@pytest.mark.parametrize("theta", np.linspace(0, np.pi / 2, 7))
def test_subensemble_predictability_visibility_saturated(theta):
    """Pure two-path case: Pred_d^2 + V_d^2 = 1 for every detector that can fire
    (Englert & Bergou 2000, eq. 78, with equality for pure states)."""
    m = kim_model(N, r=0.6, theta=theta)
    Dd, Vd = path_predictability(m), sorted_visibility(m)
    fires = m["P_detector"] > 1e-12
    np.testing.assert_allclose((Dd ** 2 + Vd ** 2)[fires], 1, atol=1e-12)


def test_sorted_visibility_matches_pattern():
    m = kim_model(N, r=0.5, theta=0.3)
    Pxd = m["P_x_given_d"]
    for d in range(2):
        col = Pxd[:, d]
        v = (col.max() - col.min()) / (col.max() + col.min())
        assert abs(v - sorted_visibility(m)[d]) < 1e-9


from isp.eraser import path_record_check


@pytest.mark.parametrize("r,theta", [(0.5, np.pi / 4), (0.2, 0.7), (1.0, 0.1), (0.0, 0.5), (0.5, 0.0)])
def test_t3_bound_is_r_sin_2theta_and_zero_before_idler_detection(r, theta):
    c = path_record_check(r=r, theta=theta)
    assert c["bound_t2"] < 1e-12 and c["defect_t2"] < 1e-12
    assert abs(c["bound_t3"] - r * abs(np.sin(2 * theta))) < 1e-12
    assert c["defect_t3"] <= c["bound_t3"] + 1e-12


def test_kim_setup_t1_is_not_a_division_event():
    c = path_record_check()
    assert c["bound_sup"] == pytest.approx(0.5)
    assert c["defect_t3"] > 0.3


@pytest.mark.parametrize("r,theta", [(0.5, np.pi / 4), (1.0, np.pi / 4), (0.3, 0.4)])
def test_signal_marginal_composes_although_no_division_event(r, theta):
    c = path_record_check(r=r, theta=theta)
    assert c["signal_marginal_defect_t2"] < 1e-12
    assert c["signal_marginal_defect_t3"] < 1e-12


@pytest.mark.parametrize("r,theta", [(0.5, np.pi / 4), (0.3, 0.4)])
def test_joint_defect_is_detector_weighted_sorted_defect(r, theta):
    m = kim_model(r=r, theta=theta)
    weighted = (np.abs(conditional_defect(m)).sum(axis=0) * m["P_detector"]).sum()
    assert abs(weighted - path_record_check(r=r, theta=theta)["defect_t3"]) < 1e-12


from isp.eraser import fringe_visibility_exact, marker_model

_rng = np.random.default_rng(20)


def _pair(overlap):
    u = np.array([1, 0], complex)
    v = np.array([overlap, np.sqrt(1 - abs(overlap) ** 2)], complex)
    Q, _ = np.linalg.qr(_rng.normal(size=(2, 2)) + 1j * _rng.normal(size=(2, 2)))
    return Q @ u, Q @ v


def _haar2():
    Q, R = np.linalg.qr(_rng.normal(size=(2, 2)) + 1j * _rng.normal(size=(2, 2)))
    return Q * (np.diag(R) / np.abs(np.diag(R)))


def test_marker_model_reduces_to_kim():
    th = np.pi / 4
    W = np.array([[np.cos(th), -np.sin(th)], [np.sin(th), np.cos(th)]], complex)
    e0 = np.array([1, 0], complex)
    m = marker_model(0.5, e0, np.array([0, 1], complex), e0, e0, W)
    k = kim_model(r=1.0, theta=th)
    np.testing.assert_allclose(m["P_joint"], k["P_joint"][:, :2], atol=1e-12)


@pytest.mark.parametrize("seed", range(40))
def test_mixed_record_gap_identity_and_gamma_only_bound(seed):
    pA = _rng.uniform(0.05, 0.95)
    mA, mB = _pair(_rng.uniform(0, 1) * np.exp(1j * _rng.uniform(0, 6.3)))
    eA, eB = _pair(_rng.uniform(0, 1) * np.exp(1j * _rng.uniform(0, 6.3)))
    m = marker_model(pA, mA, mB, eA, eB, _haar2())
    ok = m["P_detector"] > 1e-9
    Psd = m["P_s_given_d"][:, ok]
    D = np.abs(Psd[0] - Psd[1])
    V = fringe_visibility_exact(m["P_x_given_d"][:, ok])
    gap = 1 - D ** 2 - V ** 2
    np.testing.assert_allclose(gap, 4 * Psd[0] * Psd[1] * (1 - m["kappa"][ok] ** 2), atol=1e-10)
    assert (D ** 2 + V ** 2 <= 1 + 1e-10).all()
    # Gamma-only pointwise bound |Delta(x|d)| <= 2 sqrt(P(x|A) P(x|B) P(A|d) P(B|d))
    Delta = m["P_x_given_d"][:, ok] - m["P_x_given_s"] @ Psd
    Pxs = m["P_x_given_s"]
    bound = 2 * np.sqrt(np.outer(Pxs[:, 0] * Pxs[:, 1], Psd[0] * Psd[1]))
    assert (np.abs(Delta) <= bound + 1e-12).all()


def test_same_which_path_tables_different_erasability():
    """Record in the idler only vs in idler and environment: identical tables when
    the idler is read in the path basis, opposite outcomes when it is read for erasure."""
    e0, e1 = np.array([1, 0], complex), np.array([0, 1], complex)
    Wpath = np.eye(2, dtype=complex)
    Werase = np.array([[1, 1], [1, -1]], complex) / np.sqrt(2)
    erasable = dict(pA=0.5, mA=e0, mB=e1, eA=e0, eB=e0)
    locked = dict(pA=0.5, mA=e0, mB=e1, eA=e0, eB=e1)
    np.testing.assert_allclose(marker_model(W=Wpath, **erasable)["P_joint"],
                               marker_model(W=Wpath, **locked)["P_joint"], atol=1e-15)
    np.testing.assert_allclose(fringe_visibility_exact(marker_model(W=Werase, **erasable)["P_x_given_d"]), 1, atol=1e-12)
    np.testing.assert_allclose(fringe_visibility_exact(marker_model(W=Werase, **locked)["P_x_given_d"]), 0, atol=1e-12)


from isp.eraser import delay_check, per_run_record_check, trigger_predictions


@pytest.mark.parametrize("r,theta", [(0.5, np.pi / 4), (0.4, 0.3), (1.0, 0.2)])
def test_per_run_t3(r, theta):
    p = per_run_record_check(r=r, theta=theta)
    np.testing.assert_allclose(p["bound_d"][2:], 0, atol=1e-15)                 # which-path runs divide
    np.testing.assert_allclose(p["bound_given_d"][:2], abs(np.sin(2 * theta)), atol=1e-12)
    assert abs(p["bound_d"].sum() - path_record_check(r=r, theta=theta)["bound_t3"]) < 1e-12
    assert abs(p["defect_d"].sum() - path_record_check(r=r, theta=theta)["defect_t3"]) < 1e-12


@pytest.mark.parametrize("r,theta", [(0.5, np.pi / 4), (0.3, 0.5)])
def test_delay_does_no_work(r, theta):
    c = delay_check(r=r, theta=theta)
    assert c["order_difference"] < 1e-15
    assert c["bound_detected_only_D0_first"] < 1e-15
    assert c["bound_detected_only_idler_first"] < 1e-15
    assert abs(c["bound_full_joint"] - r * abs(np.sin(2 * theta))) < 1e-12
    assert abs(c["R01_visibility_actual"] - abs(np.sin(2 * theta))) < 1e-12
    assert c["R01_visibility_if_fully_divided_at_t2"] < 1e-12


def test_trigger_predictions_on_kim():
    np.testing.assert_allclose(trigger_predictions("QM")["visibility"], [1, 1, 0, 0], atol=1e-12)
    np.testing.assert_allclose(trigger_predictions("T3")["visibility"], [1, 1, 0, 0], atol=1e-12)
    np.testing.assert_allclose(trigger_predictions("T1")["visibility"], 0, atol=1e-12)
    np.testing.assert_allclose(trigger_predictions("T2", rstar=1)["visibility"], 0, atol=1e-12)
    np.testing.assert_allclose(trigger_predictions("T2", rstar=2)["visibility"], [1, 1, 0, 0], atol=1e-12)
    v = trigger_predictions("G", lam=3e7, hold=1e-8)["visibility"]
    np.testing.assert_allclose(v[:2], np.exp(-0.3), atol=1e-12)


@pytest.mark.parametrize("r,theta", [(0.5, np.pi / 4), (0.3, 0.4), (0.8, 1.1)])
def test_t3_bound_equals_englert_bergou_qe_visibility(r, theta):
    """Kim's sorting: T3 bound at t3 = V^QE(O_E) = sum_d P(d) V_d (Englert & Bergou eq. 30),
    and K = (1 - r) + r |cos 2 theta| (their eq. 25)."""
    m = kim_model(r=r, theta=theta)
    VQE = (m["P_detector"] * sorted_visibility(m)).sum()
    K = (m["P_detector"] * path_predictability(m)).sum()
    assert abs(VQE - path_record_check(r=r, theta=theta)["bound_t3"]) < 1e-12
    assert abs(K - ((1 - r) + r * abs(np.cos(2 * theta)))) < 1e-12
    assert K ** 2 + VQE ** 2 <= 1 + 1e-12


@pytest.mark.parametrize("r,theta,fires", [(0.5, np.pi / 4, False), (0.0, 0.5, True),
                                           (0.5, 0.0, True), (0.5, np.pi / 2, True), (0.3, 0.4, False)])
def test_t3_trigger_uses_the_computed_bound(r, theta, fires):
    """T3 fires (c = 0) exactly where path_record_check's bound vanishes."""
    c = trigger_predictions("T3", r=r, theta=theta)["c"]
    assert c == (0.0 if fires else 1.0)
    assert (path_record_check(r=r, theta=theta)["bound_sup"] <= 1e-9) == fires
