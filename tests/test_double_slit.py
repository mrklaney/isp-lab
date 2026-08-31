import numpy as np
import pytest

from isp.divisibility import check_divisibility_lp, divisibility_defect
from isp.double_slit import (
    double_slit_matrices,
    far_field_propagator,
    fringe_visibility,
    make_double_slit_process,
    screen_distribution,
    slit_preparation,
)


def test_far_field_propagator_is_unitary():
    U = far_field_propagator(16)
    np.testing.assert_allclose(U.conj().T @ U, np.eye(16), atol=1e-12)


def test_slit_amplitudes_are_orthonormal():
    """The defect that broke the original sinc model: non-orthogonal slit amplitudes."""
    U = far_field_propagator(24)
    a, b = U[:, 10], U[:, 13]
    assert abs(a.conj() @ a - 1) < 1e-12
    assert abs(b.conj() @ b - 1) < 1e-12
    assert abs(a.conj() @ b) < 1e-12


def test_slit_preparation_is_unitary_with_balanced_source_column():
    U1 = slit_preparation(24, 10, 13, source=0)
    np.testing.assert_allclose(U1.conj().T @ U1, np.eye(24), atol=1e-12)
    expected = np.zeros(24)
    expected[[10, 13]] = 1 / np.sqrt(2)
    np.testing.assert_allclose(np.abs(U1[:, 0]), expected, atol=1e-12)


def test_probabilities_normalise_without_rescaling():
    m = double_slit_matrices()
    for key in ("gamma_20_coherent", "gamma_20_decohered"):
        p = screen_distribution(m, key)
        assert abs(p.sum() - 1.0) < 1e-12


def test_interference_term_redistributes_and_does_not_create():
    m = double_slit_matrices()
    interference = (screen_distribution(m, "gamma_20_coherent")
                    - screen_distribution(m, "gamma_20_decohered"))
    assert abs(interference.sum()) < 1e-12


def test_fringes_match_closed_form_and_classical_is_flat():
    m = double_slit_matrices()
    n, delta = m["n_modes"], m["slit_b"] - m["slit_a"]
    k = np.arange(n)
    np.testing.assert_allclose(screen_distribution(m, "gamma_20_coherent"),
                               (1 + np.cos(2 * np.pi * k * delta / n)) / n, atol=1e-12)
    np.testing.assert_allclose(screen_distribution(m, "gamma_20_decohered"),
                               np.full(n, 1 / n), atol=1e-12)


def test_fringe_pattern_is_a_column_of_the_divisibility_defect():
    """The bridge the original notebook asserted but never computed."""
    m = double_slit_matrices()
    defect = m["gamma_20_coherent"] - m["gamma_21"] @ m["gamma_10"]
    interference = (screen_distribution(m, "gamma_20_coherent")
                    - screen_distribution(m, "gamma_20_decohered"))
    np.testing.assert_allclose(interference, defect[:, m["source"]], atol=1e-15)


def test_balanced_slits_force_rank_deficient_transition_matrix():
    """
    Unitarity saturates Cauchy-Schwarz for a balanced source column, forcing rows
    slit_a and slit_b of |U1|^2 to be equal. The inverse-based divisibility test
    is therefore structurally unavailable, not merely inconclusive.
    """
    for n in (6, 8, 16, 24):
        g10 = np.abs(slit_preparation(n, 1, n - 2)) ** 2
        np.testing.assert_allclose(g10[1], g10[n - 2], atol=1e-12)
        assert np.linalg.matrix_rank(g10) == n - 1


def test_coherent_double_slit_is_indivisible():
    result = check_divisibility_lp(make_double_slit_process(coherence=1.0))
    assert result["divisible"] is False
    assert result["failure_mode"] == "no_valid_intermediate_matrix"
    assert result["defect"] > 0.0


def test_decohered_double_slit_is_divisible_with_valid_witness():
    proc = make_double_slit_process(coherence=0.0)
    result = check_divisibility_lp(proc)
    assert result["divisible"] is True
    witness = result["witness"]
    assert witness.min() > -1e-9
    np.testing.assert_allclose(witness.sum(axis=0), 1.0, atol=1e-9)
    np.testing.assert_allclose(witness @ proc.transition_from_to(0, 1),
                               proc.transition_from_to(0, 2), atol=1e-8)


@pytest.mark.parametrize("coherence", [0.05, 0.25, 0.5, 0.75, 1.0])
def test_interference_appears_only_when_indivisible(coherence):
    """Both directions of the notebook's claim, on one model."""
    m = double_slit_matrices(coherence=coherence)
    assert fringe_visibility(screen_distribution(m)) > 0
    assert check_divisibility_lp(make_double_slit_process(coherence=coherence))["divisible"] is False


def test_no_interference_exactly_when_divisible():
    m = double_slit_matrices(coherence=0.0)
    assert fringe_visibility(screen_distribution(m)) == pytest.approx(0.0, abs=1e-12)
    assert check_divisibility_lp(make_double_slit_process(coherence=0.0))["divisible"] is True
    assert divisibility_defect(make_double_slit_process(coherence=0.0)) == 0.0


def test_visibility_equals_coherence():
    for c in np.linspace(0, 1, 11):
        m = double_slit_matrices(coherence=c)
        assert fringe_visibility(screen_distribution(m)) == pytest.approx(c, abs=1e-12)


@pytest.mark.parametrize("seed", [1, 7, 42, 99, 2026])
def test_predictions_independent_of_unitary_completion(seed):
    """Only the source column is physical; the rest of U1 is an arbitrary completion."""
    reference = double_slit_matrices(seed=7)
    m = double_slit_matrices(seed=seed)
    for key in ("gamma_20_coherent", "gamma_20_decohered"):
        np.testing.assert_allclose(screen_distribution(m, key),
                                   screen_distribution(reference, key), atol=1e-12)
    assert check_divisibility_lp(make_double_slit_process(seed=seed))["divisible"] is False


def test_coherence_out_of_range_rejected():
    with pytest.raises(ValueError):
        double_slit_matrices(coherence=1.5)
