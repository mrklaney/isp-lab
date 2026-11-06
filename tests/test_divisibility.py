import numpy as np
import pytest
from isp.stochastic import PairwiseProcess, StochasticProcess, make_markov_chain
from isp.divisibility import (
    check_divisibility,
    check_divisibility_lp,
    divisibility_defect,
    indivisibility_signature,
)


def test_markov_chain_is_divisible():
    L = np.array([[-0.5, 0.3], [0.5, -0.3]])
    times = [0.0, 0.5, 1.0, 1.5]
    proc = make_markov_chain(2, L, times)
    result = check_divisibility(proc)
    assert result["divisible"] is True
    assert result["failure_mode"] is None


def test_indivisible_process_detected_negative_entries():
    # Qubit under sigma_x rotation: indivisible at times [0, 3pi/4, 5pi/6] with omega=1
    # T_32_candidate has off-diagonal ≈ -0.111 (negative entries failure)
    from isp.quantum import make_qubit_sigmax_process
    proc = make_qubit_sigmax_process(omega=1.0,
                                     times=[0.0, 3 * np.pi / 4, 5 * np.pi / 6])
    result = check_divisibility(proc)
    assert result["divisible"] is False
    assert result["failure_mode"] == "negative_entries"


def test_indivisibility_signature_zero_for_markov():
    L = np.array([[-0.5, 0.3], [0.5, -0.3]])
    times = [0.0, 0.5, 1.0]
    proc = make_markov_chain(2, L, times)
    sig = indivisibility_signature(proc)
    assert sig < 1e-10


def test_indivisibility_signature_positive_for_quantum():
    from isp.quantum import make_qubit_sigmax_process
    proc = make_qubit_sigmax_process(omega=1.0,
                                     times=[0.0, 3 * np.pi / 4, 5 * np.pi / 6])
    sig = indivisibility_signature(proc)
    assert sig > 0.0


def test_lp_agrees_with_inverse_test_on_markov_chain():
    L = np.array([[-0.5, 0.3], [0.5, -0.3]])
    proc = make_markov_chain(2, L, [0.0, 0.5, 1.0, 1.5])
    assert check_divisibility_lp(proc)["divisible"] is True
    assert divisibility_defect(proc) == 0.0


def test_lp_agrees_with_inverse_test_on_quantum_qubit():
    from isp.quantum import make_qubit_sigmax_process
    proc = make_qubit_sigmax_process(omega=1.0,
                                     times=[0.0, 3 * np.pi / 4, 5 * np.pi / 6])
    assert check_divisibility(proc)["divisible"] is False
    assert check_divisibility_lp(proc)["divisible"] is False
    assert divisibility_defect(proc) > 0.0


def test_lp_decides_where_inverse_test_reports_singular():
    """
    A singular T(0→1) makes check_divisibility() bail out with 'singular_matrix'
    regardless of the physics. The LP test still returns a verdict.
    """
    T01 = np.array([[0.5, 0.5], [0.5, 0.5]])  # rank 1
    divisible = PairwiseProcess(
        states=["0", "1"], times=[0.0, 1.0, 2.0],
        matrices={(0, 1): T01,
                  (1, 2): np.array([[0.8, 0.3], [0.2, 0.7]]),
                  (0, 2): np.array([[0.8, 0.3], [0.2, 0.7]]) @ T01},
    )
    assert check_divisibility_lp(divisible)["divisible"] is True

    indivisible = PairwiseProcess(
        states=["0", "1"], times=[0.0, 1.0, 2.0],
        matrices={(0, 1): T01,
                  (1, 2): np.array([[0.8, 0.3], [0.2, 0.7]]),
                  (0, 2): np.array([[1.0, 0.0], [0.0, 1.0]])},
    )
    assert check_divisibility_lp(indivisible)["divisible"] is False

    # the inverse-based test cannot reach either verdict
    legacy = StochasticProcess(states=["0", "1"], transitions=[T01, np.eye(2)],
                               times=[0.0, 1.0, 2.0])
    assert check_divisibility(legacy)["failure_mode"] == "singular_matrix"


def test_inverse_test_reports_singular_as_undecided_not_indivisible():
    """
    A coin flip followed by any stochastic step is divisible (the LP finds the
    step), so the inverse test must not call it indivisible. It can't decide.
    """
    T01 = np.array([[0.5, 0.5], [0.5, 0.5]])  # rank 1
    T12 = np.array([[0.8, 0.3], [0.2, 0.7]])
    proc = StochasticProcess(states=["0", "1"], transitions=[T01, T12],
                             times=[0.0, 1.0, 2.0])
    assert check_divisibility_lp(proc)["divisible"] is True
    result = check_divisibility(proc)
    assert result["divisible"] is None
    assert result["failure_mode"] == "singular_matrix"
    assert "check_divisibility_lp" in result["message"]


def test_divisibility_defect_is_zero_only_for_divisible_processes():
    T01 = np.array([[0.7, 0.2], [0.3, 0.8]])
    T12 = np.array([[0.6, 0.1], [0.4, 0.9]])
    ok = PairwiseProcess(states=["0", "1"], times=[0.0, 1.0, 2.0],
                         matrices={(0, 1): T01, (1, 2): T12, (0, 2): T12 @ T01})
    assert divisibility_defect(ok) == 0.0

    bad = PairwiseProcess(states=["0", "1"], times=[0.0, 1.0, 2.0],
                          matrices={(0, 1): T01, (1, 2): T12, (0, 2): np.eye(2)})
    assert divisibility_defect(bad) > 0.0


def test_check_divisibility_returns_at_times_on_failure():
    from isp.quantum import make_qubit_sigmax_process
    proc = make_qubit_sigmax_process(omega=1.0,
                                     times=[0.0, 3 * np.pi / 4, 5 * np.pi / 6])
    result = check_divisibility(proc)
    assert result["at_times"] is not None
    assert len(result["at_times"]) == 3


def test_check_divisibility_lp_honors_tol():
    # Symmetric 2x2 family: a valid middle step exists iff |gap(t)| <= |gap(t')|.
    # Here the gap grows by 1e-5, so the process is (barely) indivisible; the
    # verdict must follow the caller's tol, not the solver's internal tolerance.
    def sym(lam):
        return np.array([[1 + lam, 1 - lam], [1 - lam, 1 + lam]]) / 2

    proc = PairwiseProcess(states=["0", "1"], times=[0.0, 1.0, 2.0],
                           matrices={(0, 1): sym(0.5), (0, 2): sym(0.5 + 1e-5)})
    strict = check_divisibility_lp(proc, tol=1e-8)
    loose = check_divisibility_lp(proc, tol=1e-3)
    assert strict["divisible"] is False
    assert 0 < strict["defect"] <= 1e-3
    assert loose["divisible"] is True
    assert loose["witness"] is not None
